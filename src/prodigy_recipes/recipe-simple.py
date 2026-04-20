"""Randomly label images (optionally based on a substring)."""

import os
from random import shuffle

import prodigy
from labeling.export import export
from prodigy.components.loaders import Images
from minifigures_model.constants import get_data_folder
from data.data import get_already_labeled, OPTIONS


@prodigy.recipe(
    "minifigures.simple",
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
    
    def load_stream(substring: str | None = None):
        """Load in the stream to label."""
        stream = list(Images(images_path))
        already_labeled = get_already_labeled()
        stream = [image for image in stream if image["text"] not in already_labeled]
        stream = [image for image in stream if substring in image["text"]] if substring else stream
        shuffle(stream)
        for task in stream:
            task["options"] = OPTIONS
            yield task

    def progress(ctrl, update_return_value):
        """Display the progress of the labeling session."""
        total = len(os.listdir(images_path))
        return ctrl.session_annotated / total

    def on_exit(controller):
        examples = controller.db.get_dataset(controller.session_id)
        examples = [eg for eg in examples if eg["answer"] == "accept"]
        for option in [option["id"] for option in OPTIONS]:
            count = len([eg for eg in examples if option in eg["accept"]])
            print(f"Annotated {count} {option} examples")
        export()

    return {
        "dataset": "minifigures-db",
        "view_id": "choice",
        "stream": load_stream(substring=substring),
        "progress": progress,
        "on_exit": on_exit,
        "config": { "choice_style": "multiple" },
    }

