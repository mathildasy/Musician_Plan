"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
import wavio
import librosa
from utils.lib_beat import MusicFeatures

from colorit import *
init_colorit()

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

print('='*10+'>','Opening Wave File')
wf = wave.open(sys.argv[1], 'rb')
fs = wf.getframerate()
channels = wf.getnchannels()
bytes_per_sample = wf.getsampwidth()
print(fs * bytes_per_sample/channels)

# instantiate PyAudio (1) 费时间
print('='*10+'>','Instantiate PyAudio')
p = pyaudio.PyAudio()

music_features = MusicFeatures(sys.argv[1])
try:
    lib_tempo = np.loadtxt('%s_tempo.txt'%(sys.argv[1][:-len('.wav')]))
    lib_beat = np.loadtxt('%s_beat.txt'%(sys.argv[1][:-len('.wav')]))
except:
    print('='*10+'>','Generating Tempo & Beat')
    lib_tempo, lib_beat = music_features.libBeat()

try:
    chroma = np.loadtxt('%s_chroma.txt'%(sys.argv[1][:-len('.wav')]))
except:
    print('='*10+'>','Generating Chroma')
    chroma = music_features.libChroma()


global sub_bass_max, bass_max, low_midrange_max, midrange_max, upper_midrange_max, presence_max, brilliance_max
global sub_bass_beat, bass_beat, low_midrange_beat, midrange_beat, upper_midrange_beat, presence_beat, brilliance_beat
sub_bass_max = 10
bass_max = 10
low_midrange_max = 10
midrange_max = 10
upper_midrange_max = 10
presence_max = 10
brilliance_max = 10
sub_bass_beat = False
bass_beat = False
low_midrange_beat = False
midrange_beat = False
upper_midrange_beat = False
presence_beat = False
brilliance_beat = False

chroma_piece = 0
high_ratio = 0.8
time_start = True
cont = False
current_time = 0

# Beat Detection Algo
def beat_detect(in_data, beat_time):
    audio = wavio._wav2array(channels, bytes_per_sample, in_data)

    audio_fft = np.abs((np.fft.fft(audio)[0:int(len(audio)/2)])/len(audio))
    freqs = fs*np.arange(len(audio)/2)/len(audio)

    # Frequency Ranges for each important audio group
    sub_bass_indices = [idx for idx,val in enumerate(freqs) if val >= 20 and val <= 60]
    bass_indices = [idx for idx,val in enumerate(freqs) if val >= 60 and val <= 250]
    low_midrange_indices = [idx for idx,val in enumerate(freqs) if val >= 250 and val <= 500]
    midrange_indices = [idx for idx,val in enumerate(freqs) if val >= 500 and val <= 2000]
    upper_midrange_indices = [idx for idx,val in enumerate(freqs) if val >= 2000 and val <= 4000]
    presence_indices = [idx for idx,val in enumerate(freqs) if val >= 4000 and val <= 6000]
    brilliance_indices = [idx for idx,val in enumerate(freqs) if val >= 6000 and val <= 20000]


    try:
        sub_bass = np.max(audio_fft[sub_bass_indices])
        bass = np.max(audio_fft[bass_indices])
        low_midrange = np.max(audio_fft[low_midrange_indices])
        midrange = np.max(audio_fft[midrange_indices])
        upper_midrange = np.max(audio_fft[upper_midrange_indices])
        presence = np.max(audio_fft[presence_indices])
        brilliance = np.max(audio_fft[brilliance_indices])
    except:
        return None

    global sub_bass_max, bass_max, low_midrange_max, midrange_max, upper_midrange_max, presence_max, brilliance_max
    global sub_bass_beat, bass_beat, low_midrange_beat, midrange_beat, upper_midrange_beat, presence_beat, brilliance_beat
    
    sub_bass_max = max(sub_bass_max, sub_bass)
    bass_max = max(bass_max, bass)
    low_midrange_max = max(low_midrange_max, low_midrange)
    midrange_max = max(midrange_max, midrange)
    upper_midrange_max = max(upper_midrange_max, upper_midrange)
    presence_max = max(presence_max, presence)
    brilliance_max = max(brilliance_max, brilliance)

    sub_bass_beat_print = " " * len("Sub Bass Beat")
    if sub_bass >= sub_bass_max*high_ratio and not sub_bass_beat:
        sub_bass_beat = True
        sub_bass_beat_print = "Sub Bass Beat"
        # print("Sub Bass Beat")
    elif sub_bass < sub_bass_max*.3:
        sub_bass_beat = False

    bass_beat_print = " " * len("Bass Beat")
    if bass >= bass_max*high_ratio and not bass_beat:
        bass_beat = True
        bass_beat_print = "Bass Beat"
        # print("\t\tBass Beat")
    elif bass < bass_max*.3:
        bass_beat = False

    low_midrange_print = " " * len("Low Midrange Beat")
    if low_midrange >= low_midrange_max*high_ratio and not low_midrange_beat:
        low_midrange_beat = True
        low_midrange_print = "Low Midrange Beat"
        # print("\t\t\t\tLow Midrange Beat")
    elif low_midrange < low_midrange_max*.3:
        low_midrange_beat = False

    midrange_print = " " * len("Midrange Beat")
    if midrange >= midrange_max*high_ratio and not midrange_beat:
        midrange_beat = True
        midrange_print = "Midrange Beat"
        # print("\t\t\t\t\t\tMidrange Beat")
    elif midrange >= midrange_max*.3:
        midrange_beat = False

    upper_midrange_print = " " * len("Upper Midrange Beat")
    if upper_midrange >= upper_midrange_max*high_ratio and not upper_midrange_beat:
        upper_midrange_beat = True
        upper_midrange_print = "Upper Midrange Beat"
        # print("\t\t\t\t\t\t\t\tUpper Midrange Beat")
    elif upper_midrange < upper_midrange_max*.3:
        upper_midrange_beat = False

    presence_print = " " * len("Presence Beat")
    if presence >= presence_max*high_ratio and not presence_beat:
        presence_beat = True
        presence_print = "Presence Beat"
        # print("\t\t\t\t\t\t\t\t\t\tPresence Beat")
    elif presence < presence_max*.3:
        presence_beat = False

    brilliance_print = " " * len("Brilliance Beat")
    if brilliance >= brilliance_max*high_ratio and not brilliance_beat:
        brilliance_beat = True
        brilliance_print = "Brilliance Beat"
        # print("\t\t\t\t\t\t\t\t\t\t\t\tBrilliance Beat")
    elif brilliance < brilliance_max*.3:
        brilliance_beat = False

    if beat_time:
        lib_beat_detect = 'beat'
    else:
        lib_beat_detect = ''

    global current_time
    # info = " %.2f s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s" \
    #         %(current_time,sub_bass_beat_print, bass_beat_print, \
    #             low_midrange_print, midrange_print, upper_midrange_print,\
    #             presence_print, brilliance_print,lib_beat_detect)

    global chroma_piece
    info = "%.2f s\t%s"%(current_time,lib_beat_detect)+"\t"*(chroma_piece+1)+"chroma"

    return info

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    global time_start, start, lib_beat, cont
    global chroma_piece, current_time

    if time_start: 
        start = time_info['current_time']
        time_start = False

    current_time = time_info['current_time'] - start

    data = wf.readframes(frame_count)

    if (len(lib_beat) == 0): 
        lib_beat_output = False
        
    else:
        while (lib_beat[0] < current_time):
            lib_beat = lib_beat[1:]
            if (len(lib_beat) == 0): 
                lib_beat_output = False
                break
        if (len(lib_beat) != 0): 
            if (lib_beat[0] - current_time) < 1e-1:
                beat = True
            else:
                beat = False
                cont = False
            
            if beat and (not cont): 
                lib_beat_output = True
                cont = True
            else:
                lib_beat_output = False

    frame = librosa.time_to_frames(current_time,sr=22050, hop_length=512)
    chroma_piece = np.argmax(chroma[:,frame])
    current_tempo = lib_tempo[frame]
    info = beat_detect(data, lib_beat_output)

    if current_tempo > 200:                  # red | extremely fast 
        print(color(info, Colors.red))
    elif current_tempo > 168:                # orange | very fast
        print(color(info, Colors.orange))
    elif current_tempo > 120:                # yellow | heartbeat tempo
        print(color(info, Colors.yellow))
    elif current_tempo > 108:                # green  | moderately
        print(color(info, Colors.green))
    elif current_tempo > 76:                 # blue | at a walking pace
        print(color(info, Colors.blue))
    elif current_tempo > 66:                 # purple | at ease         ## Now is playing: 금요일에 만나요....
        print(color(info, Colors.purple))                         #TODO:## 双人声难区分（有和音）男女混唱诶
                                                                        ## beat太密了，看来没有对细节把握
                                                                        ## 如何判断音色（IU声音这么甜美诶qwq
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()
