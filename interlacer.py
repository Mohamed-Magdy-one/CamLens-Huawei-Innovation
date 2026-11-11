import cv2
import numpy as np


def generate_interlaced_image(image_path, pitch_pixels, num_views, shift_step):
    """
    محرك تقطيع ودمج الصور (Core Engine)
    """
    img = cv2.imread(image_path)
    if img is None:
        return None

    height, width, channels = img.shape
    out_img = np.zeros_like(img)

    strip_width = max(0.1, pitch_pixels / num_views)
    cols = np.arange(width)

    view_map = np.floor((cols % pitch_pixels) / strip_width).astype(int)
    view_map = np.clip(view_map, 0, num_views - 1)

    for v in range(num_views):
        current_shift = (v - (num_views // 2)) * shift_step
        M = np.float32([[1, 0, current_shift], [0, 1, 0]])
        shifted_img = cv2.warpAffine(img, M, (width, height))

        mask = (view_map == v)
        out_img[:, mask] = shifted_img[:, mask]

    return out_img


def generate_calibration_pattern(width, height, pitch_pixels, num_views, shift_step=0.0):
    """
    توليد نمط المعايرة الدقيق بأبعاد الشاشة الفعلية مع دعم الإزاحة (Eye Shift)
    """
    pattern = np.zeros((height, width, 3), dtype=np.uint8)
    strip_width = max(0.1, pitch_pixels / num_views)

    # طرح الإزاحة من الأعمدة عشان الخطوط تتحرك يمين وشمال
    cols = np.arange(width) - shift_step
    view_map = np.floor((cols % pitch_pixels) / strip_width).astype(int)
    view_map = np.clip(view_map, 0, num_views - 1)

    mask = (view_map == 0)
    pattern[:, mask] = (255, 255, 255)

    return pattern