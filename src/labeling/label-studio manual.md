# Label-studio manual

## Important remarks

* Viewing the label-studio server in the browser only works properly from the online vscode IDE (not from the local vscode that is connected to the codespace)!
* The label-studio UI can often hang or be unresponsive: try refreshing the page, or rebooting the server (ctrl+C and start again)
* Managing your train/val split is up to you. Label-studio (as far as we use it) only outputs labeled/unlabeled samples.
* Each time you run the label-studio server from the terminal, make sure the appropriate environment variables are set as explained in step 1 [here](#initial-setup).

## Workflow
### Initial setup
1. Tell label-studio it is ok to use local files and point to our root dir by setting some env vars in the terminal where we will run label-studio:
```sh
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/app
```
2. Start up the label-studio server from the terminal: label-studio
3. Sign up for an account and login (email not verified, only for local purposes, we don’t need user functionality, make sure to uncheck the box to not get emails)
4. A new tab should automatically pop open with the label-studio UI
5. Create project:
    1. Enter a project name
    2. Press save upper right corner
    3. Go back to the main page
    4. Set the labeling interface:
        1. Click the 3 dots on the upper right corner of the project tab > settings > Labeling interface
        2. Copy the content from the file labeling/project_config.xml on the codespace and paste it here. Press save.
    5. Connect our image data to label-studio:
        1. Still under settings, go to Cloud Storage in the left sidebar (Yes, the local files are under cloud storage 🙃)
        2. Click ‘Add source storage’
        3. Select ‘Local files’ under ‘Storage Type’
        4. Choose a Storage Title e.g. Image dataset
        5. Specify the directory where your images are located, make sure this is an absolute path (and thus starts with /app/…)
        6. Set the File Filter Regex to .*png
        7. Enable the option ‘Treat every bucket object as a source file. This basically tells label-studio that every image corresponds with one labeling task.
        8. Press save
        9. Sync our dataset by pressing the button ‘Sync Storage’. Internally label-studio creates ‘tasks’ with metadata for every image. This can take a while. After pressing the ‘Sync Storage’ button, a runtime error may occur. The progress up until that error is not lost, simply press the button again until the status is completed.
    6. Create a target storage where the annotations will be saved to:
        1. Still under settings > Cloud Storage, click ‘Add target storage’
        2. Select ‘Local files’ under ‘Storage Type’
        3. Choose a Storage Title e.g. label-studio annotations
        4. Specify an empty directory (make sure it exists) where your annotations will be saved to, make sure this is an absolute path (and thus starts with /app/…)

## First time labeling
1. Return to the home page and click on your project.
2. We want to label at random first, need to set the box in Settings (top right) > General > Task Sampling > Random sampling. Click Save and return to the labeling page.
3. Click the blue button ‘Label All Tasks’ to start labeling. (Use the keyboard shortcuts to speed up)

## Export to simple json format
1. After labeling, the annotations are automatically saved to the target storage we set up in the beginning. The following steps export these to a simple json format with as keys the image tags and as values a list of image classes.
2. In the vscode editor, go to labeling > export_annotations.py
3. In the section `if __name__ == "__main__":`: set the correct values for the variables (dir that points to the label-studio annotations and dir that points to where dataset.json will be saved to)
4. Run the file.

## Active learning: adding k nearest neighbors of highest loss train samples
The k nearest neighbors from the trainset are searched in the unlabeled dataset. The prediction score field in label-studio for those nearest neighbors is then populated with the value of the loss for the corresponding trainset sample. By ordering the samples in label-studio on prediction score (loss), we can label the most useful images first.

1. Make sure the label-studio server is running (in a terminal session where the two required env vars are set).
2. Go to the file labeling > active_learning.py
3. Complete the functions `get_embeddings()`, `get_loss_trainset()`, `get_tags_labeled()`
4. In the section `if __name__ == "__main__":`: set the correct values for the variables:
    1. Model_version: pick a string of your choosing (e.g. model_v1)
    2. Token: go to the label-studio UI > Account & Settings (top right on the user circle) > Access Token > Press the button ‘Copy’ under the long string
    3. Project_id: go to the label-studio UI, click on your project, checkout the number after …/projects/ in the URL.
5. Run the file.
6. In order to view the correct prediction scores in the label-studio UI, we have to select the right model_version: Settings > Machine Learning > Model Version and select the appropriate one from the list. Click ‘Save’.
7. Return to the overview of annotation tasks inside your project.
8. Order by Prediction score and make sure the direction is correct (from highest to lowest if you minimize the loss). (Make sure you view the prediction score on screen by pressing the ‘Columns’ button and selecting prediction score)
9. Instead of pressing the blue button ‘Label All Tasks’, press the arrow on the blue button and press ‘Label Tasks As Displayed’.