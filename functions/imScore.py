from functions.imChange import imChange

def imScore(score):
    if score > 0.7:
        imChange('good')
    else:
        imChange('bad')