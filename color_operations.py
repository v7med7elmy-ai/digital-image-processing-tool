import cv2
import numpy as np

def change_red_lighting(image, value=50):
    result = image.copy()

    result[:, :, 2] = cv2.add(result[:, :, 2], np.array([value], dtype=np.uint8))
    return result

def swap_r_and_g(image):
    result = image.copy()
    result[:, :, 1] = image[:, :, 2] 
    result[:, :, 2] = image[:, :, 1] 
    return result

def eliminate_red(image):
    result = image.copy()
    result[:, :, 2] = 0  
    return result