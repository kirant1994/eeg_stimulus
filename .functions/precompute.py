import numpy as np
from keras.models import load_model
import scipy.io as sio
import os
# from functions import walkman
from python_speech_features import logfbank
import scipy.io.wavfile as wav
from scipy.io.wavfile import read
import scipy.io as sio
import librosa

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

def forwardPass(param_list):
    # K.clear_session()
    wav_file = param_list[0]
    model = param_list[1]
    trans = param_list[2]
    fs, utt_wav = read(wav_file)
    utt_feat = logfbank(utt_wav, samplerate=fs, lowfreq=64, highfreq=8000, nfilt=40)
    utt_feat_trans = featureTransform(utt_feat, trans)
    x = utt_feat_trans
    print(np.shape(x))
    y = model.predict(x)
    return y

model = load_model('models/japanese.h5')
trans = sio.loadmat('models/feature_transform.mat')
os.system('clear')
playback_dir = 'playback/eng'
filelist = os.listdir(playback_dir)
for filename in filelist:
    if filename[-3 :] == 'wav':
        wav_name = '{0:s}/{1:s}'.format(playback_dir, filename)
        print(wav_name)
        fs, signal = wav.read(wav_name)
        sample_feat = logfbank(signal, samplerate=fs, lowfreq=64, highfreq=8000, nfilt=40)
        sample_feat_trans = featureTransform(sample_feat, trans)
        x = sample_feat_trans
        y = model.predict(x, batch_size=512)
        sio.savemat('precomputed/eng/{0:s}'.format(filename[:-4]), {'out':y})