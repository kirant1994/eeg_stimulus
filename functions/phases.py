import numpy as np
import time
from functions.imChange import imChange
import sounddevice as sd
from functions import walkman
# from functions.score_new import score
# from functions import vad
# from functions.imScore import imScore
from functions import config

def phase1(truth, sample):
    dict = config.getPhase1()
    t = list()
    # Starting trial
    t.append(time.time())
    imChange('blank')
    data, fs = walkman.load(truth['path'])
    print('Starting trial {0:s}...'.format(truth['path']))
    while time.time() - t[0] < dict['rest1']:
        None
    # File will play after 1.5 seconds
    t.append(time.time())
    imChange('listen')
    while time.time() - t[0] < dict['rest1'] + dict['delay']:
        None
    # Playing file
    print('Playing')
    walkman.play(data, fs)
    while time.time() - t[0] < dict['rest1'] + dict['delay'] + dict['listen']:
        None
    # Rest time begins
    t.append(time.time())
    print('Rest')
    imChange('rest')
    while time.time() - t[0] < dict['rest1'] + dict['delay'] + dict['listen'] + dict['rest2']:
        None
    # Speak time
    print('Speak')
    imChange('speak')
    t.append(time.time())
    rec, fs = walkman.record_nowait(2.5, 16000, 1)
    while(time.time() - t[3] < dict['record']):
        None
    # Recording ends here. Scoring can now begin
    t.append(time.time())
    imChange('triangle')
    print('Saving')
    walkman.save(sample['path'], rec, 16000)
    imChange('blank')
    return t

def phase2a(truth, sample):
    dict = config.getPhase2a()
    t = list()
    # Starting trial
    t.append(time.time())
    imChange('blank')
    data, fs = walkman.load(truth['endpath'])
    print('Starting trial {0:s}...'.format(truth['path']))
    while time.time() - t[0] < dict['rest1']:
        None
    t.append(time.time())
    imChange(truth['image'], path=truth['impath'])
    print('Image')
    while time.time() - t[0] < dict['rest1'] + dict['image']:
        None
    imChange('listen')
    time.sleep(dict['delay'])
    # Playing file
    print('Playing')
    walkman.play(data, fs)
    while time.time() - t[0] < dict['rest1'] + dict['image'] + dict['listen']:
        None
    # Rest time begins
    t.append(time.time())
    print('Rest')
    imChange('rest')
    while time.time() - t[0] < dict['rest1'] + dict['image'] + dict['listen'] + dict['rest2']:
        None
    # Speak time
    print('Speak')
    imChange('speak')
    t.append(time.time())
    rec, fs = walkman.record_nowait(2.5, 16000, 1)
    while(time.time() - t[3] < dict['record']):
        None
    # Recording ends here. Scoring can now begin
    t.append(time.time())
    imChange('triangle')
    print('Saving')
    walkman.save(sample['path'], rec, 16000)
    imChange('blank')
    return t

def phase2b(truth, sample):#, model, trans, nnet_dict):
    dict = config.getPhase2b()
    t = list()
    # Starting trial
    t.append(time.time())
    imChange('blank')
    data, fs = walkman.load(truth['endpath'])
    print('Starting trial {0:s}...'.format(truth['path']))
    while time.time() - t[0] < dict['rest1']:
        None
    t.append(time.time())
    imChange(truth['image'], path=truth['impath'])
    print('Image')
    while time.time() - t[0] < dict['rest1'] + dict['image']:
        None
    imChange('blank')
    time.sleep(dict['rest2'])
    # Speak time
    print('Speak')
    imChange('speak')
    t.append(time.time())
    rec, fs = walkman.record_nowait(2.5, 16000, 1)
    while(time.time() - t[2] < dict['record']):
        None
    # Recording ends here. Scoring can now begin
    t.append(time.time())
    imChange('triangle')
    print('Saving')
    walkman.save(sample['path'], rec, 16000)
    # Playing file
    imChange('listen')
    print('Playing')
    walkman.play(data, fs)
    while time.time() - t[3] < dict['listen']:
        None
    # # Doing VAD
    # first = time.time()
    # # sample['path'] = 'recordings/data2.wav'
    # vad.makeVad(sample['path'], 'temp.wav')
    # sample['path'] = 'temp.wav'
    # # Scoring
    # print('Scoring')
    # sc = score(sample, truth, model, trans, nnet_dict)
    # print(sc)
    # print('Scored in {0:.2f} seconds\n'.format(time.time() - first))
    # # Show score image
    # imScore(sc)
    # time.sleep(dict['score'])
    return t

def phase3(truth, sample):
    dict = config.getPhase3()
    t = list()
    # Starting trial
    t.append(time.time())
    imChange('blank')
    data, fs = walkman.load(truth['path'])
    print('Starting trial {0:s}...'.format(truth['path']))
    while time.time() - t[0] < dict['rest1']:
        None
    # File will play after 1.5 seconds
    t.append(time.time())
    imChange('listen')
    while time.time() - t[0] < dict['rest1'] + dict['delay']:
        None
    # Playing file
    print('Playing')
    walkman.play(data, fs)
    while time.time() - t[0] < dict['rest1'] + dict['delay'] + dict['listen']:
        None
    # Rest time begins
    t.append(time.time())
    print('Rest')
    imChange('rest')
    while time.time() - t[0] < dict['rest1'] + dict['delay'] + dict['listen'] + dict['rest2']:
        None
    # Speak time
    print('Speak')
    imChange('speak')
    t.append(time.time())
    rec, fs = walkman.record_nowait(2.5, 16000, 1)
    while(time.time() - t[3] < dict['record']):
        None
    # Recording ends here. Scoring can now begin
    t.append(time.time())
    imChange('triangle')
    print('Saving')
    walkman.save(sample['path'], rec, 16000)
    imChange('blank')
    return t