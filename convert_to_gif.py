import ffmpeg
import sys

input = ffmpeg.input(sys.argv[1])
audio = input.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
video = input.video.hflip()
out = ffmpeg.output(audio, video, sys.argv[2])

