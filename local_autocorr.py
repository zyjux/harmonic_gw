import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from glob import glob
import re

def auto_correlate(img, x, y, width, height, xrange=None, yrange=None):
    if xrange==None:
        xrange = width//2
    if yrange==None:
        yrange = height//2
        
    img_crop = img[y:y+height, x:x+width]
    img_crop = (img_crop - img_crop.mean()) / img_crop.std()
    
    normalizer = np.sum(img_crop * img_crop)
    
    full_xrange = range(0, 2*xrange)
    full_yrange = range(0, 2*yrange)
    
    corr_img = np.zeros((len(full_yrange), len(full_xrange)))
    
    for xt in full_xrange:
        for yt in full_yrange:
            x_ref = x + (xt - xrange)
            y_ref = y + (yt - yrange)
            img_comp = img[y_ref:y_ref+height, x_ref:x_ref+width]
            img_comp = (img_comp - img_comp.mean()) / img_comp.std()
            corr_img[yt, xt] = np.sum(img_comp * img_crop) / normalizer
    
    corr_img[yrange, xrange] = np.NaN
            
    return corr_img


def local_auto_corr(img, width, height=None):
    if height == None:
        height = width
    
    xnum = (img.shape[1] // width) - 1
    ynum = (img.shape[0] // height) - 1
    
    x_vals = [width // 2 + i * width for i in range(xnum)]
    y_vals = [height // 2 + i * height for i in range(ynum)]
    
    corr_im = np.full(img.shape, np.NaN)
    
    for x in x_vals:
        for y in y_vals:
            corr_im_temp = auto_correlate(img, x, y, width, height)
            corr_im[y:y+corr_im_temp.shape[0], x:x+corr_im_temp.shape[1]] = corr_im_temp
            
    return corr_im


img_dir = "E:/research_data/2022_harmonic_gravity_waves/preprocessed_images/"
fn_list = glob(img_dir + "full_ims/*.png")

square_size = 50

for fn in fn_list:
    with Image.open(fn).convert('L') as raw_img:
        img = np.asarray(raw_img, dtype='float64')
        
    auto_corr_im = local_auto_corr(img, square_size)
    
    sav_fn = img_dir + "auto_corr_ims/" + re.search("\d{4}-\d{2}-\d{2}.*(?=_..._log)", fn).group() + "_auto_corr_im.jpg"
    
    F = plt.Figure()
    ax = plt.gca()
    ax.imshow(auto_corr_im)
    ax.set_xticks([])
    ax.set_yticks([])
    F.set_facecolor("white")
    plt.savefig(sav_fn, bbox_inches='tight', dpi=400)
    plt.close()
    del auto_corr_im