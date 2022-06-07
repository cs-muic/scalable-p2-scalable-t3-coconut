#!/bin/sh
START_AT_SECOND=0;

# echo "Output the GIF using the palette:"
# ffmpeg -ss $START_AT_SECOND -t 15 -i $1 -loop coconut.gif
# ffmpeg -framerate 1 -i simpimgs%03d.jpg -loop -1 simpson.gif
# ffmpeg -ss $START_AT_SECOND -t 15 -i palette.jpg output.gif

# convert -delay 2 -loop 0 palette.png -scale 480x360 $1
# ffmpeg -ss $START_AT_SECOND -t 15 -i $1 -i palette.png -filter_complex "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse" $2
convert -delay 10 -loop 0 frames/*.png $1