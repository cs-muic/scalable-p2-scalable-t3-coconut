FROM ubuntu:18.04
# LABEL Name=aciffmpeg Version=0.0.2
WORKDIR /app
RUN apt-get update
RUN apt-get -y install ffmpeg
COPY gif-composer.sh /
COPY ../extract-resize-worker/palette.png /

RUN chmod +x /gif-composer.sh

ENTRYPOINT ["/gif-composer.sh"]
CMD $1 $2