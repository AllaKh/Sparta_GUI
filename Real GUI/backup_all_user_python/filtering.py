import numpy as np

def reject_outliers_2(data, m = 2.):
    if type(data) == list:
        data = np.array(data)
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/(mdev if mdev else 1.)
    return data[s<m]