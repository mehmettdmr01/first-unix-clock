#!/usr/bin/env bash
# Recorded run (on the throwaway server): restores the disk/tape from the clean copy, opens an xterm on a virtual
# screen, records the screen to mp4 with ffmpeg while surucu.py drives the console and writes the .cast.
# Output: /root/unix/cekim/<name>.cast and <name>.mp4.   Usage: bash kaydet.sh v1|v4
set -u
AD=$1; U=/root/unix; C=$U/cekim; mkdir -p $C
if [ "$AD" = v1 ]; then cp $U/jun72b/build/rf0.dsk $U/jun72b/build/rk0.dsk $U/jun72b/images/; fi
if [ "$AD" = v4 ]; then rm -f $U/v4/disk.rk; cp $U/v4/unix_v4.tap.temiz $U/v4/unix_v4.tap; fi
pkill Xvfb; sleep 1
Xvfb :99 -screen 0 1920x1080x24 -nolisten tcp >/dev/null 2>&1 & XV=$!
sleep 2; export DISPLAY=:99
ffmpeg -y -loglevel error -f x11grab -draw_mouse 0 -video_size 1920x1080 -framerate 30 -i :99 \
  -c:v libx264 -preset ultrafast -crf 16 -pix_fmt yuv420p $C/$AD.mp4 > $C/$AD-ffmpeg.log 2>&1 & FF=$!
sleep 1
xterm -geometry 80x24+150+90 -fa "DejaVu Sans Mono" -fs 24 -bg "#111315" -fg "#E8E4D8" -bw 0 \
  -e python3 $U/surucu.py $U/final_$AD.py $C/$AD.cast
sleep 1; kill -INT $FF; wait $FF; kill $XV
ls -la $C/$AD.*
