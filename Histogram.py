import cv2
import numpy as np

def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def histogram_stretching(img_gray):
    min_val = np.min(img_gray)
    max_val = np.max(img_gray)

    stretched = (img_gray - min_val) * (255 / (max_val - min_val))
    return stretched.astype(np.uint8)

def histogram_equalization(img_gray):
    return cv2.equalizeHist(img_gray)

def global_threshold(img_gray, T=127):
    _, binary = cv2.threshold(img_gray, T, 255, cv2.THRESH_BINARY)
    return binary

def automatic_threshold(img_gray):
    _, binary = cv2.threshold(
        img_gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return binary

def adaptive_threshold(img_gray):
    binary = cv2.adaptiveThreshold(
        img_gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        11,
        2  
    )
    return binary