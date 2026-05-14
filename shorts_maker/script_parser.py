import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Scene:
    index: int
    narration: str
    subtitle: str
    image_prompt: str
    duration: Optional[float] = None
    image_path: Optional[str] = None


def parse_script(script_text: str) -> List[Scene]:
    """
    스크립트 형식:
    [SCENE]
    narration: 안녕하세요, 오늘은 파이썬을 배워볼게요.
    subtitle: 파이썬 입문
    image: 밝은 컴퓨터 화면, 코드가 보이는 배경
    duration: 4.0  (선택)
    """
    scenes = []
    blocks = re.split(r'\[SCENE\]', script_text.strip())

    for i, block in enumerate(blocks):
        if not block.strip():
            continue

        def extract(key, b=block):
            m = re.search(rf'{key}:\s*(.+)', b)
            return m.group(1).strip() if m else ""

        duration_str = extract("duration")
        scenes.append(Scene(
            index=i,
            narration=extract("narration"),
            subtitle=extract("subtitle"),
            image_prompt=extract("image"),
            duration=float(duration_str) if duration_str else None,
        ))

    return scenes
