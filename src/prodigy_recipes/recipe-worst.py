"""Prodigy recipe to label worst predictions."""

import json
import os
from random import shuffle

import prodigy
import numpy as np
from labeling.export import export
from prodigy.components.loaders import Images
from minifigures_model.constants import get_data_folder
from minifigures_model.training import MinifiguresDataset
from data.data import get_already_labeled, get_latest_model, predict_dataset, OPTIONS



@prodigy.recipe(
    "minifigures.worst",
)
def image_caption():
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

    def load_stream():
        """Load in the stream to label."""
        model = get_latest_model()
        y_pred, y_true, _ = predict_dataset(dataset, model)
        errors = np.sum(np.round(y_pred) != y_true, axis=1)
        sorter = np.argsort(errors)[::-1]
        y_pred, y_true = y_pred[sorter], y_true[sorter]

        stream = list(Images(images_path))
        tags = [sample["tag"] for sample in dataset]
        tag2ind = {image["text"]: ind for ind, image in enumerate(stream)}
        stream = [stream[tag2ind[tag]] for tag in tags]
        stream = [stream[idx] for idx in sorter]

        for task, y_true_sample in zip(stream, y_true, strict=True):
            caption = [
                cls_
                for cls_, y_pred_sample_cls in zip(dataset.classes, y_true_sample, strict=True)
                if y_pred_sample_cls
            ]
            task["options"] = OPTIONS
            task["orig_caption"] = caption
            task["accept"] = caption
            yield task

    def progress(ctrl, update_return_value):
        """Display the progress of the labeling session."""
        total = len(os.listdir(images_path))
        return ctrl.session_annotated / total

    return {
        "dataset": "minifigures-db",
        "view_id": "choice",
        "stream": load_stream(),
        "update": update,
        "progress": progress,
        "config": {
            "choice_style": "multiple",
        },
    }