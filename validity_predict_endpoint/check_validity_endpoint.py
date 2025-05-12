"""Script to test the validity of the prediction endpoint used by the students.

The returned json response body of the provided predict endpoint should be of the form:
{
  "prediction": {
    "alien": 0.5033560395240784,
    "angry": 0.4998975694179535,
    "cape": 0.4822640120983124,
    "facial hair": 0.5151089429855347,
    "glasses": 0.49567556381225586,
    "happy": 0.4752386212348938,
    "hat": 0.5000626444816589,
    "helmet": 0.5069687962532043,
    "human": 0.48360809683799744,
    "robot": 0.49168452620506287
  }
}

STEPS:
    * At the bottom of the file in the 'if __name__ == "__main__":' clause: change the variable URL to your API prediction endpoint url.
    * Put the image 'sample.png' at the same level of directory as this file.
    * Run this python file to test the validity of the endpoint. If the message "If you read this message, your endpoint is valid!" is printed in the terminal, then the endpoint is valid.

"""
import os

import requests


def test_endpoint(url: str) -> None:
    """Test the validity of the endpoint.

    Parameters
    ----------
    url : str
        The URL of the endpoint.

    Raises
    ------
    NotImplementedError
        If the URL is empty.
    FileNotFoundError
        If the sample image is not found.
    """
    if len(url) == 0:
        raise NotImplementedError("You forgot to enter your endpoint URL.")

    classes = [
        "alien",
        "angry",
        "cape",
        "facial hair",
        "glasses",
        "happy",
        "hat",
        "helmet",
        "human",
        "robot",
    ]

    im_name = "sample.png"
    im_path = os.path.join(os.path.dirname(__file__), im_name)

    if not os.path.exists(im_path):
        raise FileNotFoundError(
            "You forgot to put the sample image at the same file hierarchy level as this script."
        )

    with open(im_path, "rb") as im_file:
        resp = requests.post(
            url=url,
            files={"file": (im_name, im_file, "image/png")},  # Define file name, file, content type
        ).json()

    # Testing validity endpoint
    test1 = "prediction" in resp
    assert (
        test1
    ), f"Missing key in response: 'prediction'. Instead the following response is given:\n\n {resp}"

    pred_dict = resp["prediction"]
    test2 = set(pred_dict.keys()) == set(classes)
    assert (
        test2
    ), f"There is an error in the given classes, the keys of response['prediction'] should be the set {set(classes)}."

    test3 = all([isinstance(pred, float) for pred in pred_dict.values()])  # Prediction type
    assert (
        test3
    ), f"The predictions should be python float values, instead they have types {[type(pred) for pred in pred_dict.values()]}."


if __name__ == "__main__":
    URL = "http://0.0.0.0:8000/predict/image"  # Change this to your endpoint URL

    test_endpoint(URL)

    print("If you read this message, your endpoint is valid!")
