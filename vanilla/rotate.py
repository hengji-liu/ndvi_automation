from skimage.transform import rotate
from skimage.io import imread, imsave
from skimage.draw import polygon
import numpy as np
import configparser
import sys

# load configuration
cfg = configparser.ConfigParser()
cfg.read(sys.argv[1])
source_name = cfg.get('parameters', 'source_name')
record_name = cfg.get('parameters', 'record_name')
output_name = cfg.get('parameters', 'output_name')

plot_x = cfg.getfloat('parameters', 'plot_x')
plot_y = cfg.getfloat('parameters', 'plot_y')
net_x = cfg.getfloat('parameters', 'net_x')
net_y = cfg.getfloat('parameters', 'net_y')

angle_deg = cfg.getfloat('parameters', 'angle_deg')

x_offset = cfg.getfloat('parameters', 'x_offset')
y_offset = cfg.getfloat('parameters', 'y_offset')

rownum = cfg.getint('parameters', 'rownum')
rangenum = cfg.getint('parameters', 'rangenum')
x = cfg.getint('parameters', 'x')
y = cfg.getint('parameters', 'y')

# load image
image = imread(fname=source_name)

# rotate
image_new = rotate(image=image, angle=angle_deg, resize=True)

# find point's new position
angle_rad = angle_deg / 180 * np.pi
cos = np.cos(angle_rad)
sin = np.sin(angle_rad)
center_val = np.ceil(len(image_new) / 2)
shift = (len(image_new) - len(image)) / 2
point = np.array((x + shift, -y - shift))
center = np.array((center_val, -center_val))
matrix = np.array(((cos, -sin), (sin, cos)))
point_new = matrix.dot(point - center) + center
x = point_new[0]
y = -point_new[1]

# compute ndvi mean
vals = []
for i in range(rownum):
    for j in range(rangenum):
        _x1 = x + j * net_x + x_offset
        _y1 = y + i * net_y + y_offset
        _x2 = _x1 + plot_x
        _y2 = _y1 + plot_y
        x1 = np.ceil(_x1)
        y1 = np.ceil(_y1)
        x2 = np.ceil(_x2)
        y2 = np.ceil(_y2)
        r = np.array([y1, y1, y2, y2])
        c = np.array([x1, x2, x2, x1])
        rr, cc = polygon(r, c)
        # pseudo code for ndvi mean
        # values = []
        # for pixel in image_new[rr, cc]:
        #     values.append(pixel.ndvi)
        # vals.append(sum(values)/len(values))
        value = 0
        for pixel in image_new[rr, cc]:
            value += sum(pixel)
        vals.append(value)

# RGB sum normalisation
max = max(vals)
min = min(vals)
rrange = max - min
vals = tuple(map(lambda v: (max - v) / rrange, vals))

# draw and record
with open(record_name, 'w') as f:
    f.write('refid,row,range,val\n')
    refid = 0
    for i in range(rownum - 1, -1, -1):
        for j in range(rangenum):
            _x1 = x + j * net_x + x_offset
            _y1 = y + i * net_y + y_offset
            _x2 = _x1 + plot_x
            _y2 = _y1 + plot_y
            x1 = np.ceil(_x1)
            y1 = np.ceil(_y1)
            x2 = np.ceil(_x2)
            y2 = np.ceil(_y2)
            r = np.array([y1, y1, y2, y2])
            c = np.array([x1, x2, x2, x1])
            rr, cc = polygon(r, c)
            colour = vals[i * rangenum + j]
            image_new[rr, cc] = (colour, colour, colour)
            entry = str(refid) + ',' \
                    + str(i + 1) + ',' \
                    + str(j + 1) + ',' \
                    + str(colour) + '\n'
            f.write(entry)
            refid += 1

imsave(fname=output_name, arr=image_new)
