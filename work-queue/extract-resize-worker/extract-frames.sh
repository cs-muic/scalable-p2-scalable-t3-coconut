#!/bin/sh
START_AT_SECOND=0; # in seconds, if you want to skip the first 30 seconds put 30 here

# echo "Generate a palette:"
ffmpeg -y -ss $START_AT_SECOND -t 15 -i $1 -vf fps=30,scale=580:-1:flags=lanczos,palettegen palette.png