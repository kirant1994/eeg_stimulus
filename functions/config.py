def getGeneral():
    str2bool = {'True':True, 'False':False}
    dict = {}
    with open('data/config.txt', 'r+') as file:
        txt = file.read()
    txt = txt.split('#####################################')[0].split('-------------------------------------')[1].split('\n')
    dict['start'] = (int)(txt[1].split('\t')[-1])
    dict['break'] = (int)(txt[2].split('\t')[-1])
    dict['trials'] = (int)(txt[3].split('\t')[-1])
    dict['keypress'] = str2bool[txt[4].split('\t')[-1]]
    dict['short_break'] = (int)(txt[5].split('\t')[-1])
    dict['short_trials'] = (int)(txt[6].split('\t')[-1])
    return dict

def getPhase1():
    dict = {}
    with open('data/config.txt', 'r+') as file:
        txt = file.read()
    txt = txt.split('#####################################')[2].split('-------------------------------------')[1].split('\n')
    dict['rest1'] = (float)(txt[1].split('\t')[-1])
    dict['delay'] = (float)(txt[2].split('\t')[-1])
    dict['listen'] = (float)(txt[3].split('\t')[-1])
    dict['rest2'] = (float)(txt[4].split('\t')[-1])
    dict['record'] = (float)(txt[5].split('\t')[-1])
    return dict

def getPhase2a():
    dict = {}
    with open('data/config.txt', 'r+') as file:
        txt = file.read()
    txt = txt.split('#####################################')[3].split('-------------------------------------')[1].split('\n')
    dict['rest1'] = (float)(txt[1].split('\t')[-1])
    dict['image'] = (float)(txt[2].split('\t')[-1])
    dict['delay'] = (float)(txt[3].split('\t')[-1])
    dict['listen'] = (float)(txt[4].split('\t')[-1])
    dict['rest2'] = (float)(txt[5].split('\t')[-1])
    dict['record'] = (float)(txt[6].split('\t')[-1])
    return dict

def getPhase2b():
    dict = {}
    with open('data/config.txt', 'r+') as file:
        txt = file.read()
    txt = txt.split('#####################################')[4].split('-------------------------------------')[1].split('\n')
    dict['rest1'] = (float)(txt[1].split('\t')[-1])
    dict['image'] = (float)(txt[2].split('\t')[-1])
    dict['rest2'] = (float)(txt[3].split('\t')[-1])
    dict['record'] = (float)(txt[4].split('\t')[-1])
    dict['listen'] = (float)(txt[5].split('\t')[-1])
    dict['score'] = (float)(txt[6].split('\t')[-1])
    return dict

def getPhase3():
    dict = {}
    with open('data/config.txt', 'r+') as file:
        txt = file.read()
    txt = txt.split('#####################################')[5].split('-------------------------------------')[1].split('\n')
    dict['rest1'] = (float)(txt[1].split('\t')[-1])
    dict['delay'] = (float)(txt[2].split('\t')[-1])
    dict['listen'] = (float)(txt[3].split('\t')[-1])
    dict['rest2'] = (float)(txt[4].split('\t')[-1])
    dict['record'] = (float)(txt[5].split('\t')[-1])
    return dict