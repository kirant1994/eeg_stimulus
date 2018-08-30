import numpy as np
import time
from functions.imChange import imChange
import sounddevice as sd
from functions import walkman
from functions.score_new import score
from functions import vad

def playFile(truth, sample, model, trans, nnet_dict):
    t = list()
    
    # Starting trial
    t.append(time.time())
    imChange('blank')
    data, fs = walkman.load(truth['path'])
    print('Starting trial {0:s}...'.format(truth['path']))
    while time.time() - t[0] < 1.5:
        None
    
    # File will play after 1.5 seconds
    t.append(time.time())
    imChange('listen')
    while time.time() - t[0] < 2:
        None

    # Playing file
    print('Playing')
    walkman.play(data, fs)
    while time.time() - t[0] < 3.5:
        None
    
    # Rest time begins
    t.append(time.time())
    print('Rest')
    imChange('rest')
    while time.time() - t[0] < 5:
        None
    
    # Speak time
    print('Speak')
    imChange('speak')
    t.append(time.time())
    rec, fs = walkman.record_nowait(2.5, 16000, 1)
    while(time.time() - t[3] < 2.5):
        None
    
    # Recording ends here. Scoring can now begin
    t.append(time.time())
    imChange('triangle')
    print('Saving')
    walkman.save(sample['path'], rec, 16000)

    # Doing VAD
    first = time.time()
    # sample['path'] = 'recordings/data2.wav'
    vad.makeVad(sample['path'], 'temp.wav')
    sample['path'] = 'temp.wav'
    # Scoring
    print('Scoring')
    sc = score(sample, truth, model, trans, nnet_dict)
    print(sc)
    print('Scored in {0:.2f} seconds\n'.format(time.time() - first))
    imChange('blank')
    return t