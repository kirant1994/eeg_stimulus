import numpy as np
import os
import scipy.io as sio
from keras import backend as K
import matplotlib.pyplot as plt
from python_speech_features import logfbank
from scipy.io.wavfile import read
import multiprocessing as mp
from functions import walkman
from functions.distance import klDist
from functions.makeList import makeList
from dtw import dtw
from dtw import fastdtw
import pandas as pd
import multiprocessing as mp
# from scipy.spatial.distance import euclidean
from functions.distance import euclidean
import time
from keras.models import load_model
import json

all_model = {'eng':load_model('models/eng/model_cut.h5'), 'jap':load_model('models/jap/model_cut.h5')}
trans = {'eng':sio.loadmat('models/eng/feature_transform.mat'), 'jap':sio.loadmat('models/jap/feature_transform.mat')}
# Creating word list
labels = pd.read_excel('data/labels.xlsx')
word_list = {'eng':labels[labels['Language'] == 'eng'].values[:, 1:5], 'jap':labels[labels['Language'] == 'jap'].values[:, 1:5]}

for word in word_list:
    for row in word_list[word]:
        row[1] = 'playback/{0:s}/{1:s}'.format(word, row[2])

def doSplice(feat, splice):
    dim = np.shape(feat)
    rows = dim[0]
    cols = dim[1]
    col_new = cols * len(splice)
    feat_new = np.zeros((rows, col_new))
    for i in range(0, rows):
        for j in range(0, np.size(splice)):
            first = j * cols
            last = j * cols + cols
            curr = i + splice[j]
            ind = (int)(np.clip(curr, 0, np.shape(feat)[0]-1))
            feat_new[i, first:last] = feat[ind, :]
    return feat_new

def doAddshift(feat, addshift):
    rows = np.shape(feat)[0]
    feat_new = np.copy(feat)
    for i in range(0, rows):
        feat_new[i, :] = feat_new[i, :] + addshift
    return feat_new

def featureTransform(feat, trans):
    splice = trans['splice'].reshape(np.size(trans['splice']))
    addshift = trans['addshift'].reshape(np.size(trans['addshift']))
    rescale = trans['rescale'].reshape(np.size(trans['rescale']))
    feat_s = doSplice(feat, splice)
    feat_sa = doAddshift(feat_s, addshift)
    feat_sar = feat_sa * rescale
    return feat_sar

def run_parallel(func, arg_list, n_workers=10, p_bar=True):
    pool = mp.Pool(n_workers)
    out = pool.map(func, arg_list)
    pool.close()
    if out is not None:
        return list(out)

def getDist(args):
    sample = args['s_path']
    word = args['w_path']
    model = args['model']
    trans = args['trans']

    sample_wav, fs = walkman.load(sample)
    sample_feat = logfbank(sample_wav, samplerate=fs, lowfreq=64, highfreq=8000, nfilt=40, nfft=2048)
    sample_feat_trans = featureTransform(sample_feat, trans)

    word_wav, fs = walkman.load(word)
    word_feat = logfbank(word_wav, samplerate=fs, lowfreq=64, highfreq=8000, nfilt=40, nfft=2048)
    word_feat_trans = featureTransform(word_feat, trans)

    y_sample = model.predict(sample_feat_trans)
    y_word = model.predict(word_feat_trans)

    dist, _, _, _ = dtw(makeList(y_word), makeList(y_sample), euclidean)
    args['dist'] = dist
    return args

def load_truth(filename):
    wav_name = filename.split('/')[-1][:-4]
    folder_name = filename.split('/')[-2]
    path = 'precomputed/{0:s}/{1:s}.mat'.format(folder_name, wav_name)
    out = sio.loadmat(path)['out']
    return out

def makeFeature(args):
    sample = args['path']
    trans = args['trans']

    sample_wav, fs = walkman.load(sample)
    sample_feat = logfbank(sample_wav, samplerate=fs, lowfreq=64, highfreq=8000, nfilt=40, nfft=2048)
    sample_feat_trans = featureTransform(sample_feat, trans)
    args['feat'] = sample_feat_trans
    return args

def getDtw(args):
    dist, _, _, _ = dtw(makeList(args['w_feat']), makeList(args['s_feat']), euclidean)
    args['dist'] = dist
    return args

def getKey(item):
    return item['dist']

def makeDict():
    nnet_dict = {}
    for lang in ['eng', 'jap']:
        model = all_model[lang]
        args_for_fbank = list()

        # The sample in the 0th position is the sample word. The following 12 samples are the checklist.
        for word in word_list[lang]:
            args_for_fbank.append({'path':word[1], 'label':word[0], 'trans':trans[lang]})

        args_after_fbank = run_parallel(makeFeature, args_for_fbank, n_workers=20)
        x = None
        for arg in args_after_fbank:
            if x is None:
                x = arg['feat']
            else:
                x = np.append(x, arg['feat'], axis=0)
            # print(arg['label'], np.shape(arg['feat']))

        y = model.predict(x, batch_size=2048)

        cursor = 0
        for arg in args_after_fbank:
            length = np.shape(arg['feat'])[0]
            arg['nnet'] = y[cursor : cursor+length]
            cursor = cursor + length
        nnet_dict[lang] = args_after_fbank
    return nnet_dict