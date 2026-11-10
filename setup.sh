#!/usr/bin/env bash
# Sets up both old Unix systems on a fresh Ubuntu 24.04 machine (run it only on a throwaway server, as root).
# Everything lands in /root/unix. This is the setup the recordings in recordings/ were made with (10 November 2026).
#   1st Edition (1971-72): the unix-jun72 restoration (c3x04 fork), run on classic SIMH 3.12-5 (PDP-11/20)
#   4th Edition (1973):    the University of Utah tape (files from squoze.net), run on Open SIMH (PDP-11/45)
set -eu
U=/root/unix; mkdir -p $U; cd $U
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q build-essential git curl unzip python3-pexpect xvfb xterm ffmpeg fonts-dejavu-core

# Open SIMH, PDP-11 only (for the 4th Edition)
[ -d simh ] || git clone -q --depth 1 https://github.com/open-simh/simh.git
(cd simh && make pdp11)

# Classic SIMH 3.12-5 (for the 1st Edition: with Open SIMH 4.1 it did not reach the login prompt for me)
mkdir -p simh39 && cd simh39
[ -s simhv312-5.zip ] || curl -fsS -o simhv312-5.zip http://simh.trailing-edge.com/sources/simhv312-5.zip
unzip -q -o simhv312-5.zip && (cd sim && mkdir -p BIN && make pdp11)
cd $U

# 1st Edition: the c3x04 fork applies the init patch from the right path (the original repo's console never shows login:).
# Two fixes for today's tools: apout needs -fcommon with new GCC, and two helper scripts are Python 2 (py3yap.py ports them).
[ -d jun72b ] || git clone -q https://github.com/c3x04/Unix-1st-Edition-jun72.git jun72b
cp jun72b/tools/fixaout.py jun72b/tools/fixaout.py.orig; cp jun72b/tools/mktape.py jun72b/tools/mktape.py.orig
python3 "$(dirname "$0")/py3yap.py" jun72b/tools
cp simh39/sim/BIN/pdp11 jun72b/tools/pdp11
(cd jun72b && make CC="cc -fcommon")

# 4th Edition: the tape and the SIMH ini files
mkdir -p v4 && cd v4
for f in unix_v4.tap install.ini boot.ini; do [ -s "$f" ] || curl -fsS -o "$f" "http://squoze.net/UNIX/v4/$f"; done
cp unix_v4.tap unix_v4.tap.temiz
sha256sum unix_v4.tap
echo "ready: bash kaydet.sh v1   /   bash kaydet.sh v4"
