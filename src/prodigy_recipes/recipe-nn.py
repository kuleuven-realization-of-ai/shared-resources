"""Prodigy recipe to label unlabeled images."""

import os

import prodigy
import numpy as np
from labeling.export import export
from prodigy.components.loaders import Images
from minifigures_model.constants import get_data_folder
from minifigures_model.training import MinifiguresDataset
from data.data import get_latest_model, generate_caption, generate_multiple_caption_probs, predict_dataset, get_image, get_already_labeled, OPTIONS
from sklearn.manifold import TSNE
from sklearn.neighbors import KNeighborsClassifier


@prodigy.recipe(
    "minifigures.nn",
    k=(
        "Number of nearest neightbors",
        "option",
        "k",
        int,
    ),
)
def image_caption(k: int = 5):
    """Prodigy labeling recipe."""
    images_path = get_data_folder() / "minifigures"
    counts = {"changed": 0, "unchanged": 0}
    training = "train"
    dataset = MinifiguresDataset(
        data_f=get_data_folder(),
        resolution=256,
        balance=False,
        augment=False,
        training=training,
    )
    
    def update(answers):
        """Update when user presses save."""
        for eg in answers:
            if eg["answer"] == "accept":
                if eg["accept"] != eg["orig_caption"]:
                    counts["changed"] += 1
                else:
                    counts["unchanged"] += 1
        
        print("\nResults so far")
        print(counts["changed"], "changed")
        print(counts["unchanged"], "unchanged")

        # Also export here
        export()

    def load_stream(images_path):
        """Load in the stream to label."""
        model = get_latest_model()

        stream = list(Images(images_path))
        known_imgs = [image["tag"] for image in dataset]

        idx_lbld = np.array([i for i, image in enumerate(stream) if image["text"].replace(".png", "") in known_imgs])
        _, y_true, _ = predict_dataset(dataset, model)
        X_all = np.array([np.ravel(get_image(image["text"], max_w=200, max_h=400).cpu().detach().numpy()) for image in stream])
        print("Embedding images...")
        try:
            X_embedded = np.load(get_data_folder() / "X_embedded.npy")
            print("Loaded from saved file")
        except FileNotFoundError:
            X_embedded = TSNE(n_components=2, perplexity=50).fit_transform(X_all)
            np.save(get_data_folder() / "X_embedded.npy", X_embedded)
        X_known = X_embedded[idx_lbld, :]
        print("Fitting KNN...")
        nn = KNeighborsClassifier(n_neighbors=k)
        nn.fit(X_known, y_true)
        print("Getting predictions of current model...")
        try:
            y_preds_all = np.load(get_data_folder() / "y_preds_all.npy")
            print("Loaded from saved file")
        except FileNotFoundError:
            y_preds_all = generate_multiple_caption_probs([s["text"] for s in stream])
            np.save(get_data_folder() / "y_preds_all.npy", y_preds_all)
        y_preds_nn = np.array(nn.predict_proba(X_embedded))[:,:,1]
        y_preds_nn = y_preds_nn.reshape(y_preds_nn.shape[1], y_preds_nn.shape[0])
        errors = np.sum((y_preds_all - y_preds_nn)**2, axis=1)
        sorter = np.argsort(errors)[::-1]
        
        stream = [stream[idx] for idx in sorter]
        for i, task in enumerate(stream):
            caption = generate_caption(task["text"], class_names=[option["id"] for option in OPTIONS], model=model)
            task["options"] = OPTIONS
            task["orig_caption"] = caption
            task["accept"] = caption
            task["meta"]["y_preds_all"] = ", ".join(map(str, np.round(y_preds_all[sorter[i]], 2)))
            task["meta"]["y_preds_nn"] = ", ".join(map(str, np.round(y_preds_nn[sorter[i]], 2)))
            task["meta"]["error"] = str(errors[sorter[i]])
            yield task

    def progress(ctrl, update_return_value):
        """Display the progress of the labeling session."""
        total = len(os.listdir(images_path))
        return ctrl.session_annotated / total

    return {
        "dataset": "minifigures-db",
        "view_id": "choice",
        "stream": load_stream(images_path=get_data_folder() / "minifigures"),
        "update": update,
        "progress": progress,
        "config": {
            "choice_style": "multiple",
        },
    }