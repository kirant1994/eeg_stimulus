from functions.imChange import imChange
import time
from functions import walkman

def clkFormat(num):
    wrd = str(num)
    if len(wrd) < 2:
        return '0{0:s}'.format(wrd)
    else:
        return wrd

def sec2clk(sec):
    hrs = (int) (sec // 3600)
    sec = sec - hrs * 3600
    mins = (int) (sec // 60)
    sec = sec - mins * 60
    hrs = clkFormat(hrs)
    mins = clkFormat(mins)
    sec = clkFormat(sec)
    return '{0:s}:{1:s}:{2:s}'.format(hrs, mins, sec)

def takeBreak(sec):
    t = time.time()
    prev = t
    index = 1
    while index <=5:
        imChange('break/{0:d}'.format(6 - index))
        while time.time() - t < index * sec / 5:
            if time.time() - prev > 1:
                print(sec2clk((int)(t + 300 - time.time())), end='\r')
                prev = time.time()
            None
        index = index + 1
    imChange('break/0')
    walkman.play('playback/beep.wav')