FROM ubuntu:20.04
# LABEL Name=aciffmpeg Version=0.0.2
ADD . /app
WORKDIR /app
RUN apt-get update
RUN apt-get -y install ffmpeg
COPY ./convert_to_gif.sh /
RUN chmod +x /convert_to_gif.sh 

ENTRYPOINT ["/convert_to_gif.sh"]
CMD [ "$1", "$2" ]