FROM python:3.10
WORKDIR /usr/src/app

# install supervisord
RUN apt-get update && apt-get install -y supervisor

# copy requirements and install (so that changes to files do not mean rebuild cannot be cached)
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy all files into the container
COPY . /usr/src/app
