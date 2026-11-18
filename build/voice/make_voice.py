import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from phrases import P
from melo.api import TTS
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
m = TTS(language='KR', device='cpu'); spk = m.hps.data.spk2id['KR']
for k, t in P.items():
    mp3 = f'{out}/{k}.mp3'
    if os.path.exists(mp3): continue
    wav = f'/tmp/{k}.wav'
    m.tts_to_file(t, spk, wav, speed=1.05, quiet=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16:TP=-1.5',
                    '-ac', '1', '-ar', '24000', '-b:a', '40k', mp3], check=True)
    os.remove(wav)
print('clips', len(P))
