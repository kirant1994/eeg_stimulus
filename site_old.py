import numpy as np
import time, os
from functions.imChange import imChange
from functions.playFile import playFile
from functions import walkman
from functions.xls2list import xls2list
from functions.takeBreak import takeBreak
import scipy.io as sio
from keras.models import load_model
import pandas as pd
from functions.precompute import makeDict

# ------------------------------- #
keypress_after_break = True # Needs a manual keypress in the terminal for 'True'
start_prompt = 13
break_time = 300 # Seconds
trials_per_break = 75 # One trial is one complete cycle of playback, recording and scoring of a single .wav file
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

model = {'eng':load_model('models/eng/model_cut.h5'), 'jap':load_model('models/jap/model_cut.h5')}
trans = {'eng':sio.loadmat('models/eng/feature_transform.mat'), 'jap':sio.loadmat('models/jap/feature_transform.mat')}
nnet_dict = makeDict()

index = 0
timestamp = list()

for i, prompt in enumerate(prompts):
    if i < start_prompt - 1:
        continue
    prompt_no = prompt[0]
    truth_id = prompt[1]
    
    data = labels[labels['Id'] == truth_id].values
    label = data[0, 1]
    filename = data[0, 2]
    lang = data[0, 3]

    index = index + 1
    filepath = 'playback/{0:s}/{1:s}'.format(lang, filename)
    savepath = '{0:s}/{1:d}.wav'.format(outfolder, prompt_no)
    
    truth = {'path':filepath, 'label':label, 'lang':lang}
    sample = {'path':savepath, 'label':label, 'lang':lang}

    t = playFile(truth, sample, model, trans, nnet_dict)
    timestamp.append(t)
    sio.savemat(out_time, {'timestamp':timestamp, 'prompts':prompts})
    if index % trials_per_break == 0:
        print('Break time')
        takeBreak(break_time)
        if keypress_after_break:
            print('Press any key to continue...')
            input()
