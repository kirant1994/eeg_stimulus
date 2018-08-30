import scipy.io.wavfile as wav
import os
import sys
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import resampy

def trimSound(data, fs, start, end):
    start_frame = (int)(start * fs)
    end_frame = len(data)
    if end is not None:
        end_frame = (int)(end * fs)
    return data[start_frame:end_frame]

def play(data, fs=None, start=0, end=None, speed=1):
    if type(data) == type('Hello') and fs == None:
        data_load, fs = load(data)
        play(data_load, fs, start=start, end=end, speed=speed)
    else:
        data_trim = trimSound(data, fs, start, end)
        fs = (int)(fs * speed)
        wav.write('.temp_aud.wav', fs, data_trim)
        if sys.platform == 'darwin':
            os.system('play .temp_aud.wav 2> /dev/null')
        os.system('aplay .temp_aud.wav 2> /dev/null')
        os.system('rm .temp_aud.wav')

def record(duration, fs=16000, channels=2):
    myrec = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return myrec, fs

def record_nowait(duration, fs=16000, channels=2):
    # Starts recording but returns instantly. The data will be written even after returning
    myrec = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    return myrec, fs

def save(filename, data, fs):
    wav.write(filename, fs, data)

def load(filename, start=0, end=None):
    fs, data = wav.read(filename)
    data = trimSound(data, fs, start, end)
    return data, fs

def resample(data, old_fs, new_fs):
    return resampy.resample(data, old_fs, new_fs), new_fs

def stereo2mono(data, fs=None):
    if fs==None and type(data)==type('Hello'):
        data, fs = load(data)
    new_data = (data[:, 0] + data[:, 1]) / 2
    return new_data, fs