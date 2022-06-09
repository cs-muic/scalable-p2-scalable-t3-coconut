# FROM ubuntu:18.04
# # LABEL Name=aciffmpeg Version=0.0.2
# WORKDIR /app
# RUN apt-get update
# RUN apt-get -y install ffmpeg
# COPY extract-frames.sh /
# COPY frames/ /

# RUN chmod +x /extract-frames.sh

# ENTRYPOINT ["/extract-frames.sh"]
# CMD $1

# Build upon this image "alpine" is a lightweight distro
FROM python:3.7-alpine

# Copy requirements.txt
COPY ./requirements.txt /app/requirements.txt

# Install all the requirements
RUN pip install -r /app/requirements.txt

# Copy everthing from . to /app inside the 'box'
COPY . /app
WORKDIR /app

# How to run it when we start up the box?
CMD ["./extract-worker.py"]