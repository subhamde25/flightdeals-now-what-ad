#!/usr/bin/env bash
# Fish Audio take -> mix-ready voice: 48 kHz mono, 1.05x tempo (pitch kept), low-cut, de-mud, presence lift, gentle compression.
# Usage: bash audio/prep_vo.sh [out.wav]   (default: assets/audio/vo.wav)
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-assets/audio/vo.wav}"
ffmpeg -hide_banner -loglevel error -y -i assets/audio/vo_raw.mp3 \
  -af "aformat=sample_rates=48000:channel_layouts=mono,atempo=1.05,highpass=f=75,equalizer=f=220:t=q:w=1.2:g=-1.5,equalizer=f=3800:t=q:w=1:g=2.5,acompressor=threshold=-22dB:ratio=3:attack=4:release=90:makeup=2" \
  -ar 48000 -ac 1 "$OUT"
echo "wrote $OUT"
python tools/analyze_vo.py "$OUT"
