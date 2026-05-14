import os
import random

from moviepy import AudioFileClip, concatenate_audioclips, afx

from config import BGM_DIR, BGM_VOLUME


def get_bgm(total_duration: float):
    """BGM 폴더에서 랜덤 BGM을 선택해 루프 처리 후 반환. 파일 없으면 None."""
    if not os.path.isdir(BGM_DIR):
        return None

    bgm_files = [f for f in os.listdir(BGM_DIR) if f.endswith(".mp3")]
    if not bgm_files:
        return None

    bgm_path = os.path.join(BGM_DIR, random.choice(bgm_files))
    bgm = AudioFileClip(bgm_path).with_multiply_volume(BGM_VOLUME)

    if bgm.duration < total_duration:
        loops = int(total_duration / bgm.duration) + 1
        bgm = concatenate_audioclips([bgm] * loops)

    return bgm.subclipped(0, total_duration).with_effects([afx.AudioFadeOut(2.0)])
