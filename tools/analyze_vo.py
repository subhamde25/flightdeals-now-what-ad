"""Print the speech segments of a voice file (10 ms RMS, -42 dB gate, gaps < 60 ms merged).
Used to place captions and visual beats on the voiceover. Usage: python tools/analyze_vo.py assets/audio/vo.wav"""
import wave, numpy as np, sys
w = wave.open(sys.argv[1]); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
hop = int(sr*0.01); n = len(x)//hop
rms = np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2))+1e-9 for i in range(n)])
db = 20*np.log10(rms)
on = db > -42
# close gaps < 60ms, drop blips < 40ms
segs=[]; i=0
while i<n:
    if on[i]:
        j=i
        while j<n and on[j]: j+=1
        segs.append([i,j]); i=j
    else: i+=1
merged=[]
for s in segs:
    if merged and s[0]-merged[-1][1] < 6: merged[-1][1]=s[1]
    else: merged.append(s)
merged=[s for s in merged if s[1]-s[0]>=4]
print("dur", len(x)/sr)
for a,b in merged: print(f"{a/100:.2f}-{b/100:.2f}  ({(b-a)/100:.2f})  peak {db[a:b].max():.1f}")
