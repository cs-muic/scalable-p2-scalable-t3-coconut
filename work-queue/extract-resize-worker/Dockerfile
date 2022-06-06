FROM ubuntu:18.04
# LABEL Name=aciffmpeg Version=0.0.2
WORKDIR /app
RUN apt-get update
RUN apt-get -y install ffmpeg
COPY extract-frames.sh /

RUN chmod +x /extract-frames.sh

ENTRYPOINT ["/extract-frames.sh"]
CMD $1 $2