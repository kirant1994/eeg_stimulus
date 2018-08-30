import matlab.engine
import os

engine = matlab.engine.start_matlab()
engine.eval('addpath functions/vad', nargout=0)
engine.eval('vad(\'recordings/mobile/Beg.wav\', \'\', \'data/log\', 0.1, \'temp.wav\')', nargout=0)
os.system('rm temp.wav')
os.system('rm matlab.mat')

def makeVad(wavIn, wavOut, thres=0.2):
    engine.eval('vad(\'{0:s}\', \'\', \'data/log\', {1:.1f}, \'{2:s}\')'.format(wavIn, thres, wavOut), nargout=0)
    os.system('rm matlab.mat')