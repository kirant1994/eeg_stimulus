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

# def forwardPass(param_list):
    # # K.clear_session()
    # wav_file = param_list[0]
    # model = param_list[1]
    # trans = param_list[2]
    # fs, utt_wav = read(wav_file)
    # utt_feat = logfbank(utt_wav, samplerate=fs, lowfreq=64, highfreq=8000, nfilt=40)
    # utt_feat_trans = featureTransform(utt_feat, trans)
    # x = utt_feat_trans
    # print(np.shape(x))
    # y = model.predict(x)
    # return y

def load_truth(filename):
    wav_name = filename.split('/')[-1][:-4]
    folder_name = filename.split('/')[-2]
    path = 'precomputed/{0:s}/{1:s}.mat'.format(folder_name, wav_name)
    out = sio.loadmat(path)['out']
    return out

def score(sample, truth, model, trans):
    sample_wav, fs = walkman.load(sample)
    sample_feat = logfbank(sample_wav, samplerate=fs, lowfreq=64, highfreq=8000, nfilt=40)
    sample_feat_trans = featureTransform(sample_feat, trans)

    print(np.shape(sample_feat_trans))
    x = sample_feat_trans
    y_sample = model.predict(x, batch_size=512)
    y_truth = load_truth(truth)
    dist, _, _, _ = dtw(makeList(y_truth), makeList(y_sample), klDist)
    return dist
