"""Randomly label images (suggest labels based on model's predictions)."""

import os
from random import shuffle

import prodigy
from labeling.export import export
from prodigy.components.loaders import Images
from minifigures_model.constants import get_data_folder
from data.data import get_already_labeled, get_latest_model, generate_caption, OPTIONS



@prodigy.recipe(
    "minifigures.simple-model",
    substring=(
        "The substring that should be present in the file name when loading in the stream",
        "option",
        "s",
        str,
    ),
)
def image_caption(substring: str | None = None):
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

    def load_stream(substring: str | None = None):
        """Load in the stream to label."""
        stream = list(Images(images_path))
        already_labeled = get_already_labeled()
        stream = [image for image in stream if image["text"] not in already_labeled]
        stream = [image for image in stream if substring in image["text"]] if substring else stream
        shuffle(stream)
        model = get_latest_model()
        for task in stream:
            caption = generate_caption(
                task["text"], class_names=[option["id"] for option in OPTIONS], model=model
            )
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
        "stream": load_stream(substring=substring),
        "update": update,
        "progress": progress,
        "config": {
            "choice_style": "multiple",
        },
    }