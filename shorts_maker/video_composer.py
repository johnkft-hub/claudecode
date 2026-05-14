import os
import tempfile

from moviepy import (
    AudioFileClip, CompositeAudioClip, CompositeVideoClip,
    ImageClip, concatenate_videoclips, vfx, afx
)

from bgm_engine import get_bgm
from config import OUTPUT_DIR, VIDEO_FPS
from image_engine import get_background
from subtitle_engine import make_subtitle_frame
from tts_engine import generate_tts


def compose_scene(scene, temp_dir: str):
    """단일 장면을 VideoClip으로 합성."""
    tts_path = os.path.join(temp_dir, f"tts_{scene.index}.mp3")
    generate_tts(scene.narration, tts_path)
    tts_audio = AudioFileClip(tts_path)

    duration = scene.duration if scene.duration else tts_audio.duration + 0.3

    bg_clip = get_background(scene, duration)

    subtitle_arr = make_subtitle_frame(scene.subtitle)
    subtitle_clip = (
        ImageClip(subtitle_arr, is_mask=False)
        .with_duration(duration)
        .with_opacity(1.0)
    )

    video = CompositeVideoClip([bg_clip, subtitle_clip], size=(bg_clip.w, bg_clip.h))
    video = video.with_audio(tts_audio)
    video = video.with_effects([vfx.FadeIn(0.3), vfx.FadeOut(0.3)])

    return video


def compose_video(scenes: list, output_name: str = "shorts_output.mp4") -> str:
    """모든 장면을 하나의 MP4로 합성 후 경로 반환."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    temp_dir = tempfile.mkdtemp()
    clips = []
    try:
        clips = [compose_scene(s, temp_dir) for s in scenes]
        final = concatenate_videoclips(clips, method="compose")

        bgm = get_bgm(final.duration)
        if bgm and final.audio:
            mixed = CompositeAudioClip([final.audio, bgm])
            final = final.with_audio(mixed)
        elif bgm:
            final = final.with_audio(bgm)

        output_path = os.path.join(OUTPUT_DIR, output_name)
        final.write_videofile(
            output_path,
            fps=VIDEO_FPS,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            preset="fast",
        )
    finally:
        # 파일 핸들 해제 후 임시 폴더 삭제 (Windows 파일 잠금 방지)
        for clip in clips:
            try:
                clip.close()
            except Exception:
                pass
        import shutil, time
        for _ in range(5):
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
                break
            except Exception:
                time.sleep(0.5)

    return output_path
