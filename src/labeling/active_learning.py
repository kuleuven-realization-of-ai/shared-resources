"""Create label-studio tasks.

A task basically corresponds to an image with optional metadata such as prediction scores.
"""
from pathlib import Path

import numpy as np
from config import HOST, PORT
from label_studio_sdk import Client
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm


def add_prediction_scores_to_label_studio(
    tags_scores: dict[str, float], model_version: str, token: str, project_id: int
) -> None:
    """Add prediction score attribute to label-studio tasks.

    Make sure the model_version does not exist yet.
    The project_id can be retrieved by clicking on the project in the UI and looking at the number after /projects/ in the url.
    """
    # Set up connection to label-studio
    ls = Client(url=f"{HOST}:{PORT}", api_key=token)
    project = ls.get_project(project_id)

    # Assert model_version does not exist yet
    assert (
        model_version not in project.get_model_versions()
    ), "The model_version you provided, already exists. Choose a different one."

    # Loop over all tasks and update those that are in tags_scores
    print("Setting prediction scores in label-studio...")
    for task in project.get_tasks():
        image_path = Path(task["storage_filename"])
        tag = image_path.stem

        if tag in tags_scores:
            project.create_prediction(
                task["id"], result=[], score=tags_scores[tag], model_version=model_version
            )


def add_active_learning_scores(model_version: str, token: str, project_id: int, k: int = 5) -> None:
    """Add loss of labeled image to its k nearest neighbor images as prediction score.

    1. Sort the images in the trainset from highest to lowest loss
    2. For every trainset image: retrieve the k most similar images (embeddingwise) from the unlabeled dataset.
    3. Add prediction score attribute in the existing label-studio tasks.

    Be sure that the necessary helper functions are implemented!
    """
    # Get all labeled tags
    tags_all_label = get_tags_labeled()

    # Get worst predictions wrt loss and rank
    print("Computing loss on the trainset...\n")
    losses_tags = get_loss_trainset()
    losses, tags = list(losses_tags.values()), list(losses_tags.keys())
    sorter = np.argsort(np.array(losses))[::-1]
    tags = [tags[idx] for idx in sorter]
    losses = [losses[idx] for idx in sorter]

    # Load embeddings and put in datastructure for efficient searching
    print("Initializing k nearest neighbors...\n")
    index = get_embeddings()
    embeddings_nolabel = np.array([index[tag] for tag in index if tag not in tags_all_label])
    tags_nolabel = [tag for tag in index if tag not in tags_all_label]
    embeddings_label = np.array([index[tag] for tag in tags])
    nn = NearestNeighbors(n_neighbors=k, metric="cosine")
    nn.fit(embeddings_nolabel)

    # Loop over all labeled images
    tags_nn_loss = {}
    for embedding, loss in tqdm(
        zip(embeddings_label, losses, strict=True),
        desc="Computing nearest neighbor for every train image...",
    ):
        # Get k NN (not tag itself)
        knn = nn.kneighbors([embedding], return_distance=False)[0, :]
        for ind_knn in knn:
            tag_nn = tags_nolabel[ind_knn]
            tags_nn_loss[tag_nn] = round(loss, 4)

    # Update prediction score of nn unlabeled images with given model_version
    add_prediction_scores_to_label_studio(
        tags_nn_loss, model_version=model_version, token=token, project_id=project_id
    )


def get_embeddings() -> dict[str, list[float]]:
    """Get embeddings of all images (labeled + unlabeled) using the model.

    Return as a dictionary with key: image tag, value: embedding as a list of floats.
    """
    # Needs to be implemented by the student
    raise NotImplementedError



def get_loss_trainset() -> dict[str, float]:
    """Get loss on each trainset image using the model.

    Return as a dictionary with key: image tag, value: loss.
    """
    # Needs to be implemented by the students
    raise NotImplementedError


def get_tags_labeled() -> list[str]:
    """Get all tags of images that are already labeled."""
    # Needs to be implemented by the student
    raise NotImplementedError


if __name__ == "__main__":
    # Add active learning scores
    model_version: str = ...  # e.g. "model_v0"
    token: str = ... # e.g. "bdbdd5d499955cdddded5e3cd401f8ad622445f5"
    project_id: int = ... # e.g. 1
    add_active_learning_scores(model_version, token, project_id, k=5)
