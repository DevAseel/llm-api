# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-bullseye as base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# installing dependecies for installing python packages
RUN apt-get update

# installing packages for api
WORKDIR /usr/src/app/
COPY ./requirements.txt .
RUN [ "python3", "-m", "pip", "install", "-r", "requirements.txt" ] 

WORKDIR /usr/src/app/
COPY ./app.py .


# running optimizer
WORKDIR /usr/src/app/
ENTRYPOINT ["uvicorn","app:app"]
