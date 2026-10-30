#!/usr/bin/env bash
# Full rebuild of the ad:
#   1. render h169/index.html frame by frame (60 fps)   -> build/video_noaudio.mp4 + build/captions.srt
#   2. synthesize BGM + SFX and mix with the voiceover   -> build/mix.wav (+ build/stems/)
#   3. master to -14 LUFS / -1 dBTP (two-pass loudnorm)  -> build/master.wav
#   4. mux + copy to deliverables/ (+ contact sheet)
# Usage: bash final.sh               (everything, ~8 min on an 8 GB laptop)
#        bash final.sh --skip-video  (reuse build/video_noaudio.mp4, redo audio + mux only)
set -euo pipefail
cd "$(dirname "$0")"
NAME=FlightDeals_16x9_NowWhat
mkdir -p build deliverables

if [[ "${1:-}" != "--skip-video" ]]; then
  echo "== 1/4 render video (60 fps)"
  node render.mjs video 60 > build/render.log 2>&1 || { tail -20 build/render.log; exit 1; }
else
  echo "== 1/4 skipped: reusing build/video_noaudio.mp4"
  [[ -f build/video_noaudio.mp4 ]] || { echo "build/video_noaudio.mp4 is missing: run without --skip-video"; exit 1; }
fi

echo "== 2/4 synthesize BGM + SFX, mix with VO"
python audio/make_audio.py

echo "== 3/4 master to -14 LUFS / -1 dBTP"
STATS=$(ffmpeg -hide_banner -i build/mix.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
LN=$(echo "$STATS" | python -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -hide_banner -loglevel error -y -i build/mix.wav -af "loudnorm=I=-14:TP=-1:LRA=11:linear=true:$LN,aresample=48000" -c:a pcm_s16le build/master.wav

echo "== 4/4 mux -> deliverables/$NAME.mp4"
ffmpeg -hide_banner -loglevel error -y -i build/video_noaudio.mp4 -i build/master.wav -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart "deliverables/$NAME.mp4"
[[ -f build/captions.srt ]] && cp build/captions.srt "deliverables/$NAME.srt"
ffmpeg -hide_banner -loglevel error -y -i "deliverables/$NAME.mp4" \
  -vf "select='eq(n\,48)+eq(n\,150)+eq(n\,320)+eq(n\,470)+eq(n\,555)+eq(n\,760)+eq(n\,850)+eq(n\,950)+eq(n\,1055)+eq(n\,1240)',scale=640:-1,tile=5x2" \
  -frames:v 1 -fps_mode vfr deliverables/contact_sheet.jpg
ffmpeg -hide_banner -i "deliverables/$NAME.mp4" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" || true
echo "done: deliverables/$NAME.mp4"
