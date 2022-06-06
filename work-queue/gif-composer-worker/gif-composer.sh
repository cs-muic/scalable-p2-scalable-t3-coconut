#!/bin/sh
START_AT_SECOND=0;

# echo "Output the GIF using the palette:"
# ffmpeg -ss $START_AT_SECOND -t 15 -i $1 -loop coconut.gif
# ffmpeg -framerate 1 -i simpimgs%03d.jpg -loop -1 simpson.gif
ffmpeg -ss $START_AT_SECOND -t 15 -i palette.jpg output.gif