import os

import numpy as np
from PIL import Image
from moviepy import ImageClip

from config import IMAGE_DIR, VIDEO_HEIGHT, VIDEO_WIDTH


def load_background(image_path: str, duration: float):
    """로컬 이미지를 9:16 배경 클립으로 변환."""
    clip = ImageClip(image_path).with_duration(duration)
    clip = clip.resized(height=VIDEO_HEIGHT)
    if clip.w < VIDEO_WIDTH:
        clip = clip.resized(width=VIDEO_WIDTH)
    x_center = clip.w / 2
    clip = clip.cropped(x_center=x_center, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
    return clip


def generate_gradient_background(color1: tuple, color2: tuple, duration: float):
    """그라디언트 배경 생성 (이미지 없을 때 폴백)."""
    img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT))
    for y in range(VIDEO_HEIGHT):
        ratio = y / VIDEO_HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        for x in range(VIDEO_WIDTH):
            img.putpixel((x, y), (r, g, b))

    arr = np.array(img)
    return ImageClip(arr).with_duration(duration)


def get_background(scene, duration: float):
    """장면에 맞는 배경 클립 반환."""
    if scene.image_path and os.path.exists(scene.image_path):
        return load_background(scene.image_path, duration)

    return generate_gradient_background((20, 20, 40), (60, 20, 80), duration)
