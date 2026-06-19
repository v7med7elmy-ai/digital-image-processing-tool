import cv2
import numpy as np

def get_kernel(size=5):
    return np.ones((size, size), np.uint8)


def apply_dilation(image, kernel_size=5):
    return cv2.dilate(image, get_kernel(kernel_size), iterations=1)

def apply_erosion(image, kernel_size=5):
    return cv2.erode(image, get_kernel(kernel_size), iterations=1)

def apply_opening(image, kernel_size=5):
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, get_kernel(kernel_size))

def internal_boundary(image, kernel_size=3):
    eroded = apply_erosion(image, kernel_size)
    return cv2.subtract(image, eroded)

def external_boundary(image, kernel_size=3):
    dilated = apply_dilation(image, kernel_size)
    return cv2.subtract(dilated, image)

def morphological_gradient(image, kernel_size=3):
    return cv2.morphologyEx(image, cv2.MORPH_GRADIENT, get_kernel(kernel_size))