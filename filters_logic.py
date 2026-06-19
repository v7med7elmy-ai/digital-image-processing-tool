import cv2
import numpy as np

def apply_average_filter(image, ksize=5):
    return cv2.blur(image, (ksize, ksize))

def apply_laplacian_filter(image):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    return np.uint8(np.absolute(laplacian))

def apply_max_filter(image, ksize=5):
    kernel = np.ones((ksize, ksize), np.uint8)
    return cv2.dilate(image, kernel)

def apply_min_filter(image, ksize=5):
    kernel = np.ones((ksize, ksize), np.uint8)
    return cv2.erode(image, kernel)

def apply_median_filter(image, ksize=5):
    return cv2.medianBlur(image, ksize)

def apply_mode_filter(image, ksize=3):
    return cv2.medianBlur(image, ksize) 

def add_salt_and_pepper(image, prob=0.05):
    output = np.copy(image)
    black_pixels = np.random.random(image.shape) < prob
    white_pixels = np.random.random(image.shape) > (1 - prob)
    output[black_pixels] = 0
    output[white_pixels] = 255
    return output

def add_gaussian_noise(image, mean=0, sigma=25):
    gauss = np.random.normal(mean, sigma, image.shape).astype(np.float32)
    noisy_image = cv2.add(image.astype(np.float32), gauss)
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return noisy_image

def restore_sp_outlier(image, threshold=30):
    mean_filtered = cv2.blur(image, (3, 3))
    diff = cv2.absdiff(image, mean_filtered)
    mask = diff > threshold
    return np.where(mask, mean_filtered, image).astype(np.uint8)

def apply_image_averaging(original_gray, num_images=10):
    noisy_list = []
    for _ in range(num_images):
        noise = np.random.normal(0, 20, original_gray.shape).astype(np.uint8)
        noisy_list.append(cv2.add(original_gray, noise))
    return np.mean(noisy_list, axis=0).astype(np.uint8)