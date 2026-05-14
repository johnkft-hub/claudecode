from script_parser import parse_script
from video_composer import compose_video

SCRIPT = """
[SCENE]
narration: 안녕하세요! 오늘은 파이썬으로 자동화를 배워볼게요.
subtitle: 파이썬 자동화 입문
image: 밝은 컴퓨터 화면, 파이썬 로고
duration: 4.0

[SCENE]
narration: 먼저 필요한 라이브러리를 설치해볼게요. pip install을 사용합니다.
subtitle: pip install 시작!
image: 터미널 화면, 코드 설치 중

[SCENE]
narration: 이렇게 간단한 코드 몇 줄로 자동화가 가능합니다. 정말 쉽죠?
subtitle: 단 10줄로 자동화 완성
image: 깔끔한 파이썬 코드 화면

[SCENE]
narration: 구독과 좋아요 부탁드립니다. 다음 영상에서 만나요!
subtitle: 구독 & 좋아요 눌러주세요!
image: 밝고 친근한 마무리 화면
duration: 3.0
"""

if __name__ == "__main__":
    scenes = parse_script(SCRIPT)
    print(f"총 {len(scenes)}개 장면 파싱 완료")

    output = compose_video(scenes, output_name="my_shorts.mp4")
    print(f"영상 생성 완료: {output}")
