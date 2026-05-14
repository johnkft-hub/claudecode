import numpy as np
from PIL import Image, ImageDraw, ImageFont

from config import (
    FONT_PATH, SUBTITLE_COLOR, SUBTITLE_FONT_SIZE,
    SUBTITLE_STROKE, SUBTITLE_STROKE_WIDTH, SUBTITLE_Y_POSITION,
    VIDEO_HEIGHT, VIDEO_WIDTH,
)


def make_subtitle_frame(text: str) -> np.ndarray:
    """자막 텍스트를 투명 배경 RGBA 이미지(numpy array)로 반환."""
    img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH, SUBTITLE_FONT_SIZE)
    except OSError:
        # 폰트 파일 없을 때 기본 폰트로 폴백
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]

    x = (VIDEO_WIDTH - text_w) // 2
    y = int(VIDEO_HEIGHT * SUBTITLE_Y_POSITION)

    sw = SUBTITLE_STROKE_WIDTH
    for dx in range(-sw, sw + 1):
        for dy in range(-sw, sw + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=SUBTITLE_STROKE)

    draw.text((x, y), text, font=font, fill=SUBTITLE_COLOR)

    return np.array(img)
