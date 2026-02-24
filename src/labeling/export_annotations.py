"""Put the annotations of label-studio from the target directory in a simple json format (keys: image tags, values: list of annotated classes).

Only keep annotated samples (ignore skipped ones).
The file is saved as dataset.json in the destination directory. If the file alread exists, it is not overwritten but a timestamp is added to the filename!
"""
import json
from datetime import datetime
from pathlib import Path


def export_label_studio_annotations_to_simple_json(source_dir: Path, destination_dir: Path) -> None:
    """Convert label-studio annotations to json."""
    dataset = {}
    # Run through files in dir
    for path in source_dir.iterdir():
        # load json
        with open(path) as f:
            metadata = json.load(f)

        # Only save non-skipped samples
        if not metadata["was_cancelled"]:
            labels = metadata["result"][0]["value"]["choices"]
            image_path: str = metadata["task"]["data"]["image"]
            image_tag = image_path.split("/")[-1][:-4]  # Last slice to remove .png extension

            dataset[image_tag] = labels

    # Save dataset
    file_name = "dataset_labeled"
    dest_path = destination_dir / f"{file_name}.json"
    # If file already exists, add timestamp to filename
    if dest_path.exists():
        file_name = f"{file_name}_{datetime.now().strftime('%Y%m%dT%H%M%S')}"  # noqa: DTZ005
        dest_path = destination_dir / f"{file_name}.json"

    with open(dest_path, "w") as f:
        json.dump(dataset, f, indent=4)


if __name__ == "__main__":
    label_studio_annotations_dir: Path = ...  # e.g. Path("/app/data/data/target_annotations")
    save_dir: Path = ...  # e.g. Path("/app/data/data/")

    export_label_studio_annotations_to_simple_json(label_studio_annotations_dir, save_dir)
