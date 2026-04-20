# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

# Copy the source files into the container
WORKDIR /repo
COPY . /repo

# Install pip requirements
RUN python -m pip install -r requirements.txt

# Define the command to be run when the container is started
ENTRYPOINT ["python"]
CMD ["app/main.py"]
