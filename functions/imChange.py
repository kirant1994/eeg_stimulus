import os
import skimage.io as skio
from skimage.transform import rescale

# def imChange(im_name, path='./images'):
#     os.system('rm ./images/current.png')
#     os.system('cp {0:s}/{1:s}.png ./images/current.png'.format(path, im_name))

def imChange(im_name, path='./images'):
    img = skio.imread('{0:s}/{1:s}.png'.format(path, im_name))
    # h = img.shape[0]
    w = img.shape[1]
    # h_corr = 362
    w_corr = 364
    scale = w_corr / w
    img_new = rescale(img, scale)#, anti_aliasing=True)
    skio.imsave('images/current.png', img_new)