# pull official base image
FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

# install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install ez_setup
COPY ./web.requirements.txt .
RUN python -m pip install -r web.requirements.txt

# set work directory
WORKDIR /usr/src/app
COPY . /usr/src/app

# copy project
# COPY . .
