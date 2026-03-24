"""Prodigy recipe to include least present classes.

The labeled samples are saved to a json file in the directory where the prodigy command is run from.
To run this custom prodigy recipe, run the following command from the terminal:
    prodigy least_classes --n <value> -F <filename_recipe_code.py>
where the values between <> need to be replaced.
Don't forget to save your progress during labelling by clicking the save-to-disk icon.
When done labelling, ctrl-C the terminal process, and the json file of newly labeled samples will be saved.

To get the custom recipe running, you need to adapt the code at three places:
    * Set the correct value for the images_path variable at line 48
    * Implement the function _get_already_labeled
    * Implement the function get_least_classes
"""
import datetime as dt
import json
import os
from pathlib import Path
from random import shuffle

import prodigy
from prodigy.components.loaders import Images

OPTIONS = [
    {"id": "alien", "text": "is alien"},
    {"id": "human", "text": "is human"},
    {"id": "robot", "text": "is robot"},
    {"id": "cape", "text": "wears cape"},
    {"id": "glasses", "text": "wears glasses"},
    {"id": "hat", "text": "wears hat"},
    {"id": "helmet", "text": "wears helmet"},
    {"id": "angry", "text": "is angry"},
    {"id": "happy", "text": "is happy"},
    {"id": "facial hair", "text": "has facial hair"},
]

dataset_name = f"prodigy_data_{dt.datetime.now()}".replace(" ", "__")  # Noqa: DTZ005


@prodigy.recipe(
    "least_classes",
    n=(
        "How many of the least present classes to label data for.",
        "option",
        "n",
        int,
    ),
)
def image_caption_least_present(n: int | None = 1):
    """Label examples for the least labeled classes."""
    images_path = None  # CHANGE THIS
    if images_path is None:
        raise NotImplementedError()

    class_to_keyword = {
        "alien": ["sw", "loc", "nex"],
        "human": ["ovr", "par", "twn"],
        "robot": ["sw"],
        "cape": ["lor", "sh"],
        "glasses": ["hp", "pck"],
        "hat": ["pi", "pln"],
        "helmet": ["cas", "cty", "pln", "rac", "sc"],
        "angry": ["pb"],
        "happy": ["ovr", "par", "twn"],
        "facial hair": ["njo", "sh", "cty", "sw"],  # only some examples, not all!
    }

    def load_stream(images_path, n):
        """Load in the stream to label."""
        print("Loading in the stream..")
        print(" - Fetching")
        stream = list(Images(images_path))
        already_labeled = _get_already_labeled()
        stream = [image for image in stream if image["text"] not in already_labeled]
        least_classes = get_least_classes(n)

        print(f" - Filtering out classes {least_classes}..")
        keywords = [class_to_keyword[class_] for class_ in least_classes]
        keywords = [keyword for keyword_list in keywords for keyword in keyword_list]  # flatten
        stream = [
            image for image in stream if any(keyword in image["text"] for keyword in keywords)
        ]
        print(" - Shuffling..")
        shuffle(stream)

        print(" -  Serving..")
        for task in stream:
            task["options"] = OPTIONS
            yield task

    def on_exit(controller):
        # write the dataset to disk
        export_dataset(dataset=dataset_name, json_name=f"{dataset_name}.json")

    return {
        "dataset": dataset_name,
        "view_id": "choice",
        "stream": load_stream(images_path=images_path, n=n),
        "on_exit": on_exit,
        "config": {
            "choice_style": "multiple",
        },
    }


def export_dataset(dataset: str, json_name: str) -> None:
    """Export the dataset to file (and delete from prodigy database)."""
    print("Exporting dataset in easy-to-read format")

    # Export annotations to local directory
    print(" - Extracting database annotations")
    ann_f = Path(__file__).parent / "annotations.jsonl"
    os.system(f"prodigy db-out {dataset} > {ann_f}")

    # Reformat the annotations
    print(" - Loading in as JSON")
    with open(ann_f) as f:
        files = [json.loads(x.strip()) for x in f.readlines() if x.strip()]
    ann_f.unlink(missing_ok=True)
    print(" - Formatting")
    result = {}
    for file in files:
        if file["answer"] == "accept":
            result[file["text"]] = sorted(file["accept"])

    # Storing data in dedicated json file
    path = json_name
    print(f" - Writing away {len(result)} samples")
    with open(path, "w") as f:
        json.dump(result, f, indent=2)


def _get_already_labeled() -> list[str]:
    """Get the image tags of already labeled images.

    Returns a list of image tag strings, e.g. ["sw0231", "col361"].
    """
    already_labeled = []

    raise NotImplementedError()

    return already_labeled


def get_least_classes(n: int | None = 1) -> list[str]:
    """Get the n classes with the least labeled data.

    Returns a list of n class strings, e.g. (for n=2) ["glasses", "hat"].
    """
    least_classes = []

    raise NotImplementedError()

    return least_classes
