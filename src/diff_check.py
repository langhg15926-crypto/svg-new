import cv2
import numpy as np


def compare_images(src_png, svg_png, diff_png):
    src = cv2.imread(str(src_png), cv2.IMREAD_GRAYSCALE)
    svg = cv2.imread(str(svg_png), cv2.IMREAD_GRAYSCALE)
    svg = cv2.resize(svg, (src.shape[1], src.shape[0]))

    diff = cv2.absdiff(src, svg)
    diff_ratio = np.mean(diff > 20)
    cv2.imwrite(str(diff_png), diff)
    return diff_ratio
