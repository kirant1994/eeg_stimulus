import skimage.io as skio
import os

filelist = os.listdir('jap_jpg')

for file in filelist:
    img = skio.imread('jap_jpg/{0:s}'.format(file))
    new_filename = '{0:s}.png'.format(file.split('.')[0])
    print(new_filename)
    skio.imsave('jap/{0:s}'.format(new_filename), img)