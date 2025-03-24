# How to run a CICD pipeline for your application?

This guide will show you how to run a CICD pipeline for your application using 
GitHub Actions and Docker. We will rely on the template CICD files provided in
the `src` folder of this repository.

## Create your GitHub Actions secrets.

If you give a look at the template CICD files provided, you will notice that they 
rely on some secrets that you need to create manually in your GitHub repository.
The idea is to avoid hardcoding sensitive information in the CICD files and hence
storing them in your Git repository, making them public.

In our case, you will need to create three secrets:

* `AWS_ACCESS_KEY_ID`: The AWS access key ID of the IAM user that will be used to interact with AWS.
  This is required by the `aws` CLI but also by Terraform. You can fetch this value in your CodeSpace
  by running:
  ```
  cat ~/.aws/credentials
  ```

* `AWS_SECRET_ACCESS_KEY`: The AWS secret access key of the IAM user that will be used to to interact 
   with AWS. This is required by the `aws` CLI but also by Terraform.You can fetch this value in your
   CodeSpace by running:
  ```
  cat ~/.aws/credentials
  ```

* `AWS_SSH_KEY`: The **private** SSH key that will be used to connect to the EC2 instance running the   
   application. This is required to allow your CICD pipeline to connect to your EC2 instance via SSH
   and run the deployment commands. Note that this is the **private** key, not the public one as your
   public key is already in the EC2 instance via the AWS SSH keypair you manually created. You can
    fetch this value in your CodeSpace by running (make sure to copy the entire content of the file
    including the `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----` lines):
    ```
    cat ~/.ssh/id_rsa
    ```

To create the secrets, head to the `Settings` tab of your GitHub repository and click on the 
`Secrets and variables` submenu in the left menu of the Settings page. Select the `Actions` section and
then click on `New repository secret`. There, fill the form with the name of the secret and its value.

![github_settings](img/github_settings.png)
![action_secrets](img/action_secrets.png)
![action_secrets_creation](img/action_secrets_creation.png)

## Create the folder structure required by GitHub Actions.

GitHub Actions requires a specific folder structure to run the CICD pipeline.
You can use the template CICD files provided above and place them in a newly created
`.github/workflows` folder at the root of your repository: 

```
├── .github # <---- Create this folder and its subfolders.
│   └── workflows
│       ├── deploy.yml
│       └── test.yml
├── infrastructure
├── Dockerfile
├── README.md
├── src
└── ...
```

In the `test.yml` and `deploy.yml` CICD template files, you will need to fill in different sections
to make them work for your application. The sections to fill in are marked with `< Write ... >` comments.

## Trigger the CICD pipelines.

Once you have created the secrets and the folder structure required by GitHub Actions, you can trigger
the pipelines simply by following their activation conditions declared under the `on` key of their YAML
files:

* The `test.yml` file will run the tests of your application when a new commit is pushed to a pull 
  request open with the `main` branch as target.

* The `deploy.yml` file will run the deployment of your application when a new tag with format `v*.*.*`
  (e.g. `v0.0.123` or `v1.0.0`) is pushed to the `main` branch. To push a tag to your repository, you
  can use the following workflow:

    ```
    git checkout main
    git pull origin main
    git tag v0.0.1
    git push --tag
    ```

Feel free to modify those conditions to run as you wish them to (e.g. run the deployment on every merge 
to the `main` branch instead of the manual tag creation process).