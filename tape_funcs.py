import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from tqdm.autonotebook import tqdm
import scipy


### Collection of functions to compute TAPE on a grayscale image
# Written by Lander Ver Hoef
# June 2023


### sample_box_disp:
# Designed to take in similar inputs to the other functions in this script,
# then plot a box from which the parallel lines are sampled.
# args:
#    center_pt: center of the box
#    angle: angle of the line samples, in standard unit circle orientation
#    width: how wide the box is
#    sample_length: how long the box is
#    color: what color the box is
# returns:
#    box: a matplotlib patch that can be applied to an image
def sample_box_disp(center_pt, angle, width=50, sample_length=200, color='red', alpha=1):
    offset_vec = np.add(
        (-sample_length/2*np.cos(angle), -sample_length/2*np.sin(angle)),
        (-width/2*np.cos(angle + np.pi/2), -width/2*np.sin(angle + np.pi/2))
    )
    corner = np.add(center_pt, offset_vec)
    box = mpl.patches.Rectangle(
        corner,
        width=sample_length,
        height=width,
        angle=np.degrees(angle),
        rotation_point='xy',
        fill=False,
        ec=color,
        alpha=alpha,
        lw=2)
    return box


# sample_line: takes in a center point and an angle and returns evenly spaced coordinates along a line of the given length and angle. 
# The values start on the left for angles in the (-pi/2, pi/2) range.
# Note that for images shown with the origin at the top, angles increase clockwise
# At sample_ratio = 1 and angle a multiple of pi/2, this will pull actual pixels with no interpolation.
# Returns a tuple (x_coords, y_coords) of coordinate lists.
def sample_line(center_pt, angle, length=200, sample_ratio=1):
    start = np.subtract(center_pt, (length/2 * np.cos(angle), length/2 * np.sin(angle)))
    end = np.add(center_pt, (length/2 * np.cos(angle), length/2 * np.sin(angle)))
    return np.linspace(start[0], end[0], int(sample_ratio*length)), np.linspace(start[1], end[1], int(sample_ratio*length))


# parallel_line_vals:
# Using sample_line, extract samples from within a given box
# args:
#    center_pt: center of the entire sample
#    angle: angle of the parallel sample lines
#    width: how wide the batch of parallel lines should be
#    width_ratio: how densely the width should be sampled
#    sample_length: how many pixels long the sample lines should be
#    sample_ratio: how densely each sample line should be sampled
#    crop: whether to crop the image down to increase the speed of map_coordinates
# If crop is set, crops the image down to just the size needed for the lines (plus 20 pixels on each side for map_coordinate's interplation) to speed up computation significantly; the speed of map_coordinates seems to be sensitive to input size
# First finds a line of length given by width through the center point perpendicular to the parallel lines and computes center points (center_x, center_y) for the parallel lines
# The interpolated values from the ith line are stored in the ith row of the line_vals matrix
def parallel_line_vals(img, center_pt, angle, width=50, width_ratio=1/5, sample_length=200, sample_ratio=1, crop=True, pro_bar=True):
    if crop:
        radius = int(np.ceil(max(width/2, sample_length/2))) + 20
        start, end = (np.subtract(center_pt, radius), np.add(center_pt, radius))
        _img = img[start[1]:end[1], start[0]:end[0]]
        _center = np.subtract(center_pt, start)
    else:
        _img = img
        _center = center_pt
    center_x, center_y = sample_line(_center, angle + np.pi/2, width, width_ratio)
    line_vals = np.empty((int(width*width_ratio), sample_length*sample_ratio))
    for i in tqdm(range(int(width*width_ratio)), disable=not pro_bar):
        line_x, line_y = sample_line((center_x[i], center_y[i]), angle, sample_length, sample_ratio)
        line_vals[i, :] = scipy.ndimage.map_coordinates(_img, np.vstack((line_y, line_x)))
    return line_vals


# TAPE_raw:
# For the given number of angles, extract sets of parallel lines from an underlying image and store them in an array.
# args:
#   img: the image being sampled; assumed to be a numpy array
#   center_pt: where the sampling is centered
#   num_angles: how many angles are sampled, evenly spaced between -pi/2 and pi/2
#   width: how wide each box is, where width is in the direction perpendicular to the sample lines
#   width_ratio: how frequently to sample in the width direction - the algorithm performs best if this is less than 1 and when width*width_ratio is an integer.
#   sample_length: how many pixels each sample line should be
#   sample_ratio: how often each line should be sampled
#   crop: whether the image should be cropped down before sampling - this can yield significant speed increases for large scenes
#   plot: whether or not the boxes should be plotted on a matplotlib plot; if True, plot_ax must be specified
#   plot_ax: the matplotlib axis object on which the boxes should be plotted
def TAPE_raw(
    img,
    center_pt,
    num_angles=8,
    width=50,
    width_ratio=1/5,
    sample_length=200,
    sample_ratio=1,
    crop=True,
    plot=False,
    plot_ax=None
):
    if plot:
        cmap = mpl.colormaps['plasma']
        colors = [cmap(col) for col in np.linspace(0, 1, num_angles+1)[:-1]]
    if crop:
        radius = int(np.ceil(max(width/2, sample_length/2))) + 20
        start, end = (np.subtract(center_pt, radius), np.add(center_pt, radius))
        _img = img[start[1]:end[1], start[0]:end[0]]
        _center = np.subtract(center_pt, start)
    else:
        _img = img
        _center = center_pt
    raw_samples = np.empty((int(width*width_ratio ), sample_length, num_angles))
    angles = np.linspace(-np.pi/2, np.pi/2, num_angles + 1)[:-1]
    for i, angle in enumerate(tqdm(angles)):
        if plot:
            plot_ax.add_patch(sample_box_disp(center_pt, angle, width=width, sample_length=sample_length, color=colors[i]))
        raw_samples[:, :, i] = parallel_line_vals(
            _img,
            _center,
            angle,
            width=width,
            width_ratio=width_ratio,
            sample_length=sample_length,
            sample_ratio=sample_ratio,
            crop=False,
            pro_bar=False
        )
    return raw_samples
