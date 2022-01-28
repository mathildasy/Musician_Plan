import librosa
import soundfile as sf
import numpy as np



class MusicFeatures():

    def __init__(self, file_name):
        self.file_name = file_name
        self.y, self.sr = librosa.load(file_name)
        self.harmonic = None
        self.percussive = None
        
    def convertHPSS(self,file_name, margin1 = 1.0, margin2 = 1.0):
        margin1, margin2 =  float(margin1), float(margin2)
        self.harmonic, self.percussive = librosa.effects.hpss(self.y,margin=(margin1, margin2))

        sf.write('%s_harmonic_(%.1f).wav'%(file_name[:-len('.wav')],margin1), self.harmonic, self.sr)
        sf.write('%s_percussive_(%.1f).wav'%(file_name[:-len('.wav')],margin2), self.percussive, self.sr)

        return self.harmonic, self.percussive, self.sr


    def libBeat(self):
        _, y, sr = self.convertHPSS(self.file_name)
        onset_env = librosa.onset.onset_strength(y, sr=sr)
        times = librosa.times_like(onset_env, sr=sr)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env,sr=sr)
        beats_time = times[beats]

        dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr,
                            aggregate=None)
        
        # save results
        np.savetxt('%s_tempo.txt'%(self.file_name.split('.')[0]), dtempo)
        print('Save Tempo to Text')

        np.savetxt('%s_beat.txt'%(self.file_name.split('.')[0]), beats_time)
        print('Save Beat to Text')
        return dtempo, beats_time


    def libChroma(self):
        if self.harmonic is None:
            y, _, _ = self.convertHPSS(self.file_name)
        else:
            y = self.harmonic
        chroma_cq = librosa.feature.chroma_cqt(y=y, sr=self.sr)
        # save results
        np.savetxt('%s_chroma.txt'%(self.file_name.split('.')[0]), chroma_cq)
        print('Save Chroma to Text')
        return chroma_cq