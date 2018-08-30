import scipy.io as sio
import numpy as np
from keras.models import load_model
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense
from keras import backend as K
import os

def truncateModel(model, layer_num):
    mdl = Sequential()
    for i in range(0, layer_num - 1):
        layer = model.layers[i]
        weights = layer.get_weights()
        activation = '{}'.format(layer.activation).split(' ')[1].split(' ')[0]
        out_dim = np.shape(weights[0])[1]
        in_dim = np.shape(weights[0])[0]
        mdl.add(Dense(out_dim, input_dim=in_dim, activation=activation, weights=weights))
    layer = model.layers[layer_num - 1]
    weights = layer.get_weights()
    activation = '{}'.format(layer.activation).split(' ')[1].split(' ')[0]
    out_dim = np.shape(weights[0])[1]
    in_dim = np.shape(weights[0])[0]
    mdl.add(Dense(out_dim, input_dim=in_dim, activation='linear', weights=weights))
    mdl.compile(loss='binary_crossentropy', optimizer='adam', metric=['accuracy'])
    mdl.save('.mdl.h5')
    mdl = load_model('.mdl.h5')
    os.system('rm .mdl.h5')
    return mdl

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.system('clear')

K.clear_session()
csj = load_model('models/csj/model.h5')
wsj = load_model('models/wsj/model.h5')

csj_cut = truncateModel(csj, 6)
csj_cut.save('models/csj/model_cut.h5')

wsj_cut = truncateModel(wsj, 6)
wsj_cut.save('models/wsj/model_cut.h5')