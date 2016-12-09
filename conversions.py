"""RGB to HSL and HSL to RGB transformations for 3D color images.

References:
[1] http://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/
[2] http://www.rapidtables.com/convert/color/rgb-to-hsl.htm

"""

import numpy as np


# reshape rgb volume to 2D
def rgb2hsl(data):
    """Convert rgb to hue saturation luminance for pseudo-color data."""
    # global flat
    # data = flat
    r = np.squeeze(data[:, 0])
    g = np.squeeze(data[:, 1])
    b = np.squeeze(data[:, 2])

    # Find luminance
    rgbMin = np.min(data, 1)
    rgbMax = np.max(data, 1)
    lum = (rgbMin + rgbMax) / 2

    # If Luminance < 0.5, then Saturation = (max-min)/(max+min)
    # If Luminance > 0.5, then Saturation = (max-min)/(2.0-max-min)
    sat = np.zeros(lum.shape)
    idx = np.arange(0, lum.size)

    # TODO: according to one saturation formula[1]:
    # iss = idx[np.where((lum > 0) & (lum <= 0.5))]  # small saturation
    # ils = idx[np.where(lum > 0.5)]  # large saturation
    # sat[iss] = (rgbMax[iss] - rgbMin[iss]) / (rgbMax[iss] + rgbMin[iss])
    # sat[ils] = (rgbMax[ils] - rgbMin[ils]) / (2.0 - rgbMax[ils] - rgbMin[ils])

    # TODO: according to another saturation formula[2]:
    ins = idx[np.where(lum > 0)]  # non zero saturation
    sat[ins] = (rgbMax[ins] - rgbMin[ins]) / (1.0 - np.abs(2*lum[ins] - 1))

    izs = idx[np.where(lum == 0)]  # zero saturation
    sat[izs] = 0
    sat = np.nan_to_num(sat)

    maxDim = np.argmax(data, 1)
    imR = [maxDim == 0]  # index maximum for red
    imG = [maxDim == 1]  # index maximum for green
    imB = [maxDim == 2]  # index maximum for blue

    # If Red is max, then Hue = (G-B)/(max-min)
    # If Green is max, then Hue = 2.0 + (B-R)/(max-min)
    # If Blue is max, then Hue = 4.0 + (R-G)/(max-min)
    hue = np.zeros(lum.shape)
    hue[imR] = (g[imR] - b[imR]) / (rgbMax[imR] - rgbMin[imR])
    hue[imG] = 2.0 + (b[imG] - r[imG]) / (rgbMax[imG] - rgbMin[imG])
    hue[imB] = 4.0 + (r[imB] - g[imB]) / (rgbMax[imB] - rgbMin[imB])

    hue = np.nan_to_num(hue)

    # Multiply hue by 60 to convert it to degrees on the color circle
    hue = (hue*60.) % 360

    data[:, 0] = hue
    data[:, 1] = sat
    data[:, 2] = lum
    return data


def hsl2rgb(data):
    """Convert hsl to rgb for pseudo-color data."""
    hue, sat, lum = data[:, 0], data[:, 1], data[:, 2]
    rgb = np.zeros(data.shape)

    # if saturation is zero assign the shades of gray to channels
    rgb[sat == 0, 0] = lum[sat == 0]
    rgb[sat == 0, 1] = lum[sat == 0]
    rgb[sat == 0, 2] = lum[sat == 0]

    # if luminance is < 0.5 (50%) then temp_1 = lum * (1.0 + sat)
    temp_1 = np.zeros(lum.shape)
    temp_1[lum < 0.5] = lum[lum < 0.5] * (1.0 + sat[lum < 0.5])
    # if luminance is >= 0.5 (50%) then temp_1 = lum + sat - lum*sat
    temp_1[lum >= 0.5] = lum[lum >= 0.5] + sat[lum >= 0.5] \
        - lum[lum >= 0.5] * sat[lum >= 0.5]
    temp_2 = 2.0 * lum - temp_1

    # hue
    hue = hue / 360.0
    # all values need to be between 0 and 1
    temp_R = (np.copy(hue) + 1.0/3.0) % 1.0
    temp_G = (np.copy(hue)) % 1.0
    temp_B = (np.copy(hue) - 1.0/3.0) % 1.0

    def correctRGB(temp_channel, temp_1, temp_2):
        """Derive correct RGB values from temporary RGB derived from hue."""
        idx_t1 = (temp_channel*6.0) < 1.0
        idx_t2 = (temp_channel*2.0) < 1.0
        idx_t2[idx_t1] = False  # if conditions in vectorized form
        idx_t3 = (temp_channel*3.0) < 2.0
        idx_t3[idx_t1] = False
        idx_t3[idx_t2] = False
        idx_t4 = (temp_channel*3.0) >= 2.0
        idx_t4[idx_t1] = False
        idx_t4[idx_t2] = False
        idx_t4[idx_t3] = False

        # test 1
        temp_channel[idx_t1] = temp_2[idx_t1] \
            + (temp_1[idx_t1] - temp_2[idx_t1]) \
            * 6.0 * temp_channel[idx_t1]

        # test 2
        temp_channel[idx_t2] = temp_1[idx_t2]

        # test 3
        temp_channel[idx_t3] = temp_2[idx_t3] \
            + (temp_1[idx_t3] - temp_2[idx_t3]) \
            * 6.0 * (2.0/3.0 - temp_channel[idx_t3])

        # test 4
        temp_channel[idx_t4] = temp_2[idx_t4]

        return temp_channel

    # apply RGB correction to each temporary channel
    temp_R = correctRGB(temp_R, temp_1, temp_2)
    temp_G = correctRGB(temp_G, temp_1, temp_2)
    temp_B = correctRGB(temp_B, temp_1, temp_2)

    rgb[sat > 0, 0] = temp_R[sat > 0]
    rgb[sat > 0, 1] = temp_G[sat > 0]
    rgb[sat > 0, 2] = temp_B[sat > 0]

    return rgb
