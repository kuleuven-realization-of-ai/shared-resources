"""Prodigy recipe to label unlabeled images."""

import os

import prodigy
import numpy as np
from labeling.export import export
from prodigy.components.loaders import Images
from minifigures_model.constants import get_data_folder
from data.data import get_latest_model, generate_caption, generate_multiple_caption_probs, OPTIONS



@prodigy.recipe(
    "minifigures.confused",
)
def image_caption():
    """Prodigy labeling recipe."""
    images_path = get_data_folder() / "minifigures"
    counts = {"changed": 0, "unchanged": 0}
    
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
        y_preds = generate_multiple_caption_probs([s["text"] for s in stream])
        confusion = np.sum(np.abs(y_preds - .5), axis=1)
        sorter = np.argsort(confusion)
        stream = [stream[idx] for idx in sorter]

        for i, task in enumerate(stream):
            caption = generate_caption(task["text"], class_names=[option["id"] for option in OPTIONS], model=model)
            task["options"] = OPTIONS
            task["orig_caption"] = caption
            task["accept"] = caption
            task["meta"]["preds"] = ", ".join(map(str, np.round(y_preds[sorter[i]], 2)))
            task["meta"]["confusion"] = str(np.round(confusion[sorter[i]], 2))
            yield task

    def progress(ctrl, update_return_value):
        """Display the progress of the labeling session."""
        total = len(os.listdir(images_path))
        return ctrl.session_annotated / total


    return {
        "dataset": "minifigures-db",
        "view_id": "choice",
        "stream": load_stream(images_path=get_data_folder() / "subset"),
        "update": update,
        "progress": progress,
        "config": {
            "choice_style": "multiple",
        },
    }