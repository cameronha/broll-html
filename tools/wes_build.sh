#!/bin/zsh
# Join a chapter card and its set with a blurred whip pan: wes_build.sh CARD.mp4 SET.mp4 OUT.mp4
a=$1; b=$2; out=$3; off=1.05; d=0.22
ffmpeg -v error -y -i $a -i $b -filter_complex "[0:v]settb=AVTB,fps=24000/1001[a];[1:v]settb=AVTB,fps=24000/1001[b];[a][b]xfade=transition=slideleft:duration=$d:offset=$off,split[m][n];[n]avgblur=sizeX=36:sizeY=1[bl];[m][bl]overlay=enable='between(t,$off,$off+$d)',format=yuv420p[v]" -map "[v]" -c:v libx264 -crf 18 $out
