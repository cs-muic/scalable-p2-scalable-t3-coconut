#!/bin/sh


# http://eyeofmidas.wordpress.com/2014/06/03/how-to-record-desktop-images-into-gif-format-on-ubuntu-14-04/

# TODO: Show some progress
# TODO: Stop for "editing"


ffmpeg -ss 30 -t 10 -i $1 -vf "fps=30,scale=580:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 $2