#!/bin/sh
START_AT_SECOND=0;

# echo "Output the GIF using the palette:"
ffmpeg -ss $START_AT_SECOND -t 15 -i $1 -i palette.png -filter_complex "fps=30,scale=580:-1:flags=lanczos[x];[x][1:v]paletteuse" $2