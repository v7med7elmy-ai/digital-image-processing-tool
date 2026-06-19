import cv2
import numpy as np

def apply_addition(image, image2=None, value=50):
    if image2 is not None:
        image2_resized = cv2.resize(image2, (image.shape[1], image.shape[0]))
        return cv2.add(image, image2_resized)
    matrix = np.ones(image.shape, dtype="uint8") * value
    return cv2.add(image, matrix)

def apply_subtraction(image, image2=None, value=50):
    if image2 is not None:
        image2_resized = cv2.resize(image2, (image.shape[1], image.shape[0]))
        return cv2.subtract(image, image2_resized)
    matrix = np.ones(image.shape, dtype="uint8") * value
    return cv2.subtract(image, matrix)

def apply_division(image, image2=None, value=2):
    if image2 is not None:
        image2_resized = cv2.resize(image2, (image.shape[1], image.shape[0]))
        image2_safe = np.where(image2_resized == 0, 1, image2_resized)
        return cv2.divide(image, image2_safe)
    if value == 0:
        value = 1
    return (image // value).astype(np.uint8)

def apply_complement(image):
    return cv2.bitwise_not(image)