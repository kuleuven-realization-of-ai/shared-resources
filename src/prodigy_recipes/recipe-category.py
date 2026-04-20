"""Prodigy recipe to label unlabeled images."""

import json
import os
from random import shuffle

import prodigy
import numpy as np
from labeling.export import export
from prodigy.components.loaders import Images
from minifigures_model.constants import get_data_folder
from data.data import get_already_labeled, get_latest_model, generate_caption, generate_caption_probs, OPTIONS


CLASS_TO_KEYWORD = {
    "alien": ["sw", "loc", "nex"],
    "human": ["ovr", "par", "twn"],
    "robot": ["sw"],
    "cape": ["lor", "sh"],
    "glasses": ["hp", "pck"],
    "hat": ["pi", "pln"],
    "helmet": ["cas", "cty", "pln", "rac", "sc"],
    "angry": ["pb"],
    "happy": ["ovr", "par", "twn"],
    "facial hair": ["njo", "sh", "cty", "sw"],
}

@prodigy.recipe(
    "minifigures.category",
    n=(
        "How many least present classes to include",
        "option",
        "n",
        int,
    ),
)
def image_caption(n: int | None = 1):
    """Prodigy labeling recipe."""
    images_path = get_data_folder() / "minifigures"
    counts = {"changed": 0, "unchanged": 0}

    def update(answers):
        for eg in answers:
            if eg["answer"] == "accept":
                if eg["accept"] != eg["orig_caption"]:
                    counts["changed"] += 1
                else:
                    counts["unchanged"] += 1
        
        # Also export here
        print("\nResults")
        print(counts["changed"], "changed")
        print(counts["unchanged"], "unchanged")
        export()

    def load_stream(images_path):
        """Load in the stream to label."""
        stream = list(Images(images_path))
        already_labeled = get_already_labeled()

        keywords = set([k for i in CLASS_TO_KEYWORD.values() for k in i])
        labeled_frac_per_keyword = { 
            key: len([im for im in already_labeled if key in im]) /
            len([im for im in stream if key in im["text"]]) for key in keywords 
        }
        keywords = sorted(labeled_frac_per_keyword)[:n]
        print("Labeled fractions:")
        print(labeled_frac_per_keyword)
        
        stream = [image for image in stream if image["text"] not in already_labeled]
        stream = [image for image in stream if any(keyword in image["text"] for keyword in keywords)]
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
        "stream": load_stream(images_path=get_data_folder() / "minifigures"),
        "update": update,
        "progress": progress,
        "config": {
            "choice_style": "multiple",
        },
    }