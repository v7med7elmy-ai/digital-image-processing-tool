import streamlit as st
import cv2
import numpy as np
from PIL import Image

import point_operations as po
import color_operations as co
import Histogram as hs
import filters_logic as fl
import edge_detection as ed
import morphology_logic as ml

st.set_page_config(page_title="Image Processing App", layout="wide")
st.title(" Image Processing Project")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png", "bmp"])

operation_categories = {
    "Point Operations": ["Addition", "Subtraction", "Division", "Complement"],
    "Color Operations": ["Change Red Lighting", "Swap R and G", "Eliminate Red"],
    "Histogram & Thresholding": ["Stretching", "Equalization", "Global Threshold", "Auto Threshold (Otsu)", "Adaptive Threshold"],
    "Spatial Filters": ["Average Filter", "Laplacian Filter", "Max Filter", "Min Filter", "Median Filter", "Mode Filter"],
    "Noise Reduction": ["S&P Median Filter", "S&P Outlier", "S&P Average Filter", "Gaussian Averaging", "Gaussian Average Filter"],
    "Edge Detection": ["Sobel Detector"],
    "Morphological Operations": ["Dilation", "Erosion", "Opening", "Internal Boundary", "External Boundary", "Morphological Gradient"]
}

col_cat, col_op = st.columns(2)
with col_cat:
    category = st.selectbox("Select Operation Category", list(operation_categories.keys()))
with col_op:
    choice = st.selectbox("Select Operation", operation_categories[category])

result = None
input_display = None

if uploaded_file is not None:

    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image_bgr = cv2.imdecode(file_bytes, 1)
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    img_color = image_bgr.copy()
    img_gray_copy = image_gray.copy()
    input_display = img_color

    image2_bgr = None
    val = None
    if choice in ["Addition", "Subtraction", "Division"]:
        mode = st.radio("Operation Mode", ["One Photo", "Two Photos"])
        if mode == "Two Photos":
            uploaded_file_2 = st.file_uploader("Upload Second Image", type=["jpg", "jpeg", "png", "bmp"])
            if uploaded_file_2 is not None:
                file_bytes_2 = np.asarray(bytearray(uploaded_file_2.read()), dtype=np.uint8)
                image2_bgr = cv2.imdecode(file_bytes_2, 1)
        else:
            val = st.slider("Value", 1, 255, 50 if choice != "Division" else 2)

    if choice == "Addition":
        result = po.apply_addition(img_color, image2_bgr, value=val if val else 50)
    elif choice == "Subtraction":
        result = po.apply_subtraction(img_color, image2_bgr, value=val if val else 50)
    elif choice == "Division":
        result = po.apply_division(img_color, image2_bgr, value=val if val else 2)
    elif choice == "Complement":
        result = po.apply_complement(img_color)
    elif choice == "Change Red Lighting":
        val = st.slider("Red Lighting Value", 0, 255, 50)
        result = co.change_red_lighting(img_color, value=val)
    elif choice == "Swap R and G":
        result = co.swap_r_and_g(img_color)
    elif choice == "Eliminate Red":
        result = co.eliminate_red(img_color)
    elif choice == "Stretching":
        result = hs.histogram_stretching(img_gray_copy)
    elif choice == "Equalization":
        result = hs.histogram_equalization(img_gray_copy)
    elif choice == "Global Threshold":
        threshold_val = st.slider("Threshold Value", 0, 255, 127)
        result = hs.global_threshold(img_gray_copy, T=threshold_val)
    elif choice == "Auto Threshold (Otsu)":
        result = hs.automatic_threshold(img_gray_copy)
    elif choice == "Adaptive Threshold":
        result = hs.adaptive_threshold(img_gray_copy)
    elif choice == "Average Filter":
        ksize = st.slider("Kernel Size", 1, 31, 5, step=2)
        result = fl.apply_average_filter(img_color, ksize=ksize)
    elif choice == "Laplacian Filter":
        result = fl.apply_laplacian_filter(img_gray_copy)
    elif choice == "Max Filter":
        ksize = st.slider("Kernel Size", 1, 31, 5, step=2)
        result = fl.apply_max_filter(img_color, ksize=ksize)
    elif choice == "Min Filter":
        ksize = st.slider("Kernel Size", 1, 31, 5, step=2)
        result = fl.apply_min_filter(img_color, ksize=ksize)
    elif choice == "Median Filter":
        ksize = st.slider("Kernel Size", 1, 31, 5, step=2)
        result = fl.apply_median_filter(img_color, ksize=ksize)
    elif choice == "Mode Filter":
        ksize = st.slider("Kernel Size", 1, 31, 3, step=2)
        result = fl.apply_mode_filter(img_color, ksize=ksize)
    elif choice == "S&P Average Filter":
        prob = st.slider("Noise Probability", 0.0, 1.0, 0.05, step=0.01)
        ksize = st.slider("Kernel Size", 1, 31, 5, step=2)
        noisy = fl.add_salt_and_pepper(img_gray_copy, prob=prob)
        result = fl.apply_average_filter(noisy, ksize=ksize)
    elif choice == "S&P Median Filter":
        prob = st.slider("Noise Probability", 0.0, 1.0, 0.05, step=0.01)
        ksize = st.slider("Kernel Size", 1, 31, 5, step=2)
        noisy = fl.add_salt_and_pepper(img_gray_copy, prob=prob)
        result = fl.apply_median_filter(noisy, ksize=ksize)
    elif choice == "S&P Outlier":
        prob = st.slider("Noise Probability", 0.0, 1.0, 0.05, step=0.01)
        threshold = st.slider("Outlier Threshold", 0, 255, 30)
        noisy = fl.add_salt_and_pepper(img_gray_copy, prob=prob)
        result = fl.restore_sp_outlier(noisy, threshold=threshold)
    elif choice == "Gaussian Averaging":
        num_images = st.slider("Number of Images to Average", 2, 50, 10)
        result = fl.apply_image_averaging(img_gray_copy, num_images=num_images)
    elif choice == "Gaussian Average Filter":
        mean = st.slider("Noise Mean", -100.0, 100.0, 0.0)
        sigma = st.slider("Noise Sigma", 0.1, 100.0, 25.0)
        ksize = st.slider("Kernel Size", 1, 31, 5, step=2)
        noisy = fl.add_gaussian_noise(img_gray_copy, mean=mean, sigma=sigma)
        result = fl.apply_average_filter(noisy, ksize=ksize)
    elif choice == "Sobel Detector":
        ksize = st.slider("Kernel Size", 1, 7, 3, step=2)
        result = ed.apply_sobel(img_color, ksize=ksize)
    elif choice == "Dilation":
        ksize = st.slider("Kernel Size", 1, 31, 5, step=2)
        result = ml.apply_dilation(img_gray_copy, kernel_size=ksize)
    elif choice == "Erosion":
        ksize = st.slider("Kernel Size", 1, 31, 5, step=2)
        result = ml.apply_erosion(img_gray_copy, kernel_size=ksize)
    elif choice == "Opening":
        ksize = st.slider("Kernel Size", 1, 31, 5, step=2)
        result = ml.apply_opening(img_gray_copy, kernel_size=ksize)
    elif choice == "Internal Boundary":
        ksize = st.slider("Kernel Size", 1, 31, 3, step=2)
        result = ml.internal_boundary(img_gray_copy, kernel_size=ksize)
    elif choice == "External Boundary":
        ksize = st.slider("Kernel Size", 1, 31, 3, step=2)
        result = ml.external_boundary(img_gray_copy, kernel_size=ksize)
    elif choice == "Morphological Gradient":
        ksize = st.slider("Kernel Size", 1, 31, 3, step=2)
        result = ml.morphological_gradient(img_gray_copy, kernel_size=ksize)

    col1, col2 = st.columns(2)
    with col1:
        st.header("Input Image")
        if input_display is not None:
            if len(input_display.shape) == 3:
                st.image(cv2.cvtColor(input_display, cv2.COLOR_BGR2RGB), use_container_width=True)
            else:
                st.image(input_display, use_container_width=True, channels="GRAY")
    with col2:
        st.header(f"Result: {choice}")
        if result is not None:
            if len(result.shape) == 3:
                st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), use_container_width=True)
            else:
                st.image(result, use_container_width=True, channels="GRAY")
else:
    st.info("Upload an image to run the selected operation.")