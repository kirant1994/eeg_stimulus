import numpy as np
import time, os
from functions.imChange import imChange
# from functions.playFile import playFile
from functions import walkman
from functions.xls2list import xls2list
from functions.takeBreak import takeBreak
import scipy.io as sio
# from keras.models import load_model
import pandas as pd
# from functions.precompute import makeDict
from functions.phases import phase1
from functions.phases import phase2a
from functions.phases import phase2b
from functions.phases import phase3
from functions import config

# ------------------------------- #
dict = config.getGeneral()

keypress_after_break = dict['keypress'] # Needs a manual keypress in the terminal for 'True'
start_prompt = dict['start']
break_time = dict['break'] # Seconds
short_break_time = dict['short_break']
trials_per_break = dict['trials'] # One trial is one complete cycle of playback, recording and scoring of a single .wav file
trials_per_short_break = dict['short_trials']
open_site = False # Automatically opens the site
# ------------------------------- #

imChange('blank')
if open_site:
    os.system('xdg-open main.html')
os.system('clear')
prompts = xls2list('data/prompts.xlsx')

labels = pd.read_excel('data/labels.xlsx')

print('Enter subject number : ')
subject = 'S{0:s}'.format(input())
outfolder = 'recordings/{0:s}'.format(subject)
out_time = 'timestamp/{0:s}.mat'.format(subject)
os.system('mkdir -p {0:s}'.format(outfolder))

# model = {'eng':load_model('models/eng/model_cut.h5'), 'jap':load_model('models/jap/model_cut.h5')}
# trans = {'eng':sio.loadmat('models/eng/feature_transform.mat'), 'jap':sio.loadmat('models/jap/feature_transform.mat')}
# nnet_dict = makeDict()

index = 0
timestamp = list()

for i, prompt in enumerate(prompts):
    if i < start_prompt - 1:
        continue
    prompt_no = int(prompt[0])
    print('Prompt no. : {0:d}'.format(prompt_no))
    truth_id = int(prompt[1])
    phase = prompt[2]
    block = prompt[3]
    
    data = labels[labels['Id'] == truth_id].values
    label = data[0, 1]
    filename = data[0, 2]
    endword = data[0, 3]
    image = str(data[0, 4]).split('.png')[0]
    lang = data[0, 5]

    index = index + 1
    filepath = 'playback/{0:s}/{1:s}'.format(lang, filename)
    endpath = 'playback/{0:s}/{1:s}'.format(lang, endword)
    savepath = '{0:s}/{1:d}.wav'.format(outfolder, prompt_no)
    
    truth = {'path':filepath, 'label':label, 'lang':lang, 'image':image, 'impath':'images/{0:s}/'.format(lang), 'endpath':endpath, 'block':block}
    sample = {'path':savepath, 'label':label, 'lang':lang}

    if phase == 1:
        t = phase1(truth, sample)
    elif phase == 2.1:
        t = phase2a(truth, sample)
    elif phase == 2.2:
        t = phase2b(truth, sample)#, model, trans, nnet_dict)
    else:
        t = phase3(truth, sample)
    # t = playFile(truth, sample, model, trans, nnet_dict)
    timestamp.append(t)
    sio.savemat(out_time, {'timestamp':timestamp, 'prompts':prompts})
    if prompt_no % trials_per_break == 0:
        print('Break time')
        takeBreak(break_time)
        if keypress_after_break:
            print('Press any key to continue...')
            input()
    elif prompt_no % trials_per_short_break == 0:
        print('Short break')
        takeBreak(short_break_time)
