# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

EXPOSE 52603

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH "${PYTHONPATH}:/app"

# Install pip requirements
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install ez_setup
COPY pyro-server.requirements.txt .
RUN python -m pip install -r pyro-server.requirements.txt

WORKDIR /app
COPY . /app
