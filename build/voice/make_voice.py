import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from phrases import P
from melo.api import TTS
import json
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
# 문장이 바뀐 음성만 다시 만든다 (텍스트 기록 파일)
MF = os.path.join(out, '_texts.json')
try: TX = json.load(open(MF, encoding='utf-8'))
except Exception: TX = {}
SINO = ('soon-', 'arr-', 'next-', 'first-')
for k, t in P.items():
    old = TX.get(k)
    if old is None and (k.startswith(SINO) or k == 'last'): old = '?'   # 예전 숫자 읽기(하나·둘) 음성 → 다시 만듦
    if old is not None and old != t and os.path.exists(f'{out}/{k}.mp3'): os.remove(f'{out}/{k}.mp3')
m = TTS(language='KR', device='cpu'); spk = m.hps.data.spk2id['KR']
for k, t in P.items():
    mp3 = f'{out}/{k}.mp3'
    if os.path.exists(mp3): continue
    wav = f'/tmp/{k}.wav'
    m.tts_to_file(t, spk, wav, speed=1.05, quiet=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16:TP=-1.5',
                    '-ac', '1', '-ar', '24000', '-b:a', '40k', mp3], check=True)
    os.remove(wav)
json.dump({k: P[k] for k in P}, open(MF, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('clips', len(P))
