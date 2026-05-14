import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from script_parser import parse_script
from video_composer import compose_video

DEFAULT_SCRIPT = """\
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

SCENE_TEMPLATE = """\
[SCENE]
narration:
subtitle:
image:
duration:
"""


class ShortsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("쇼츠 영상 자동 제작기")
        self.geometry("900x700")
        self.resizable(True, True)
        self._build_ui()

    # ── UI 구성 ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        self._build_toolbar()
        self._build_main_pane()
        self._build_bottom_bar()

    def _build_toolbar(self):
        bar = tk.Frame(self, bd=1, relief=tk.RAISED)
        bar.pack(fill=tk.X)

        tk.Button(bar, text="장면 추가", command=self._add_scene).pack(side=tk.LEFT, padx=4, pady=3)
        tk.Button(bar, text="초기화", command=self._reset_script).pack(side=tk.LEFT, padx=4, pady=3)
        tk.Button(bar, text="불러오기", command=self._load_file).pack(side=tk.LEFT, padx=4, pady=3)
        tk.Button(bar, text="저장하기", command=self._save_file).pack(side=tk.LEFT, padx=4, pady=3)

    def _build_main_pane(self):
        pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        pane.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # 왼쪽: 스크립트 편집기
        left = tk.Frame(pane)
        pane.add(left, minsize=400)

        tk.Label(left, text="스크립트 편집", font=("", 10, "bold")).pack(anchor=tk.W)
        self.script_box = scrolledtext.ScrolledText(left, wrap=tk.WORD, font=("Consolas", 10))
        self.script_box.pack(fill=tk.BOTH, expand=True)
        self.script_box.insert(tk.END, DEFAULT_SCRIPT)

        # 오른쪽: 미리보기 + 설정
        right = tk.Frame(pane)
        pane.add(right, minsize=260)

        tk.Label(right, text="장면 미리보기", font=("", 10, "bold")).pack(anchor=tk.W)
        self.preview_box = scrolledtext.ScrolledText(
            right, wrap=tk.WORD, font=("", 9), state=tk.DISABLED,
            bg="#f5f5f5", height=14
        )
        self.preview_box.pack(fill=tk.BOTH, expand=True)
        tk.Button(right, text="미리보기 갱신", command=self._refresh_preview).pack(fill=tk.X, pady=(4, 8))

        # 출력 파일명
        fn_frame = tk.LabelFrame(right, text="출력 파일명")
        fn_frame.pack(fill=tk.X, padx=2, pady=2)
        self.output_var = tk.StringVar(value="my_shorts.mp4")
        tk.Entry(fn_frame, textvariable=self.output_var).pack(fill=tk.X, padx=4, pady=4)

    def _build_bottom_bar(self):
        bottom = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        bottom.pack(fill=tk.X, side=tk.BOTTOM)

        self.progress = ttk.Progressbar(bottom, mode="indeterminate")
        self.progress.pack(fill=tk.X, padx=6, pady=(4, 2))

        self.status_var = tk.StringVar(value="준비됨")
        tk.Label(bottom, textvariable=self.status_var, anchor=tk.W).pack(fill=tk.X, padx=6)

        btn_frame = tk.Frame(bottom)
        btn_frame.pack(fill=tk.X, padx=6, pady=4)
        self.run_btn = tk.Button(
            btn_frame, text="영상 생성 시작", bg="#2196F3", fg="white",
            font=("", 11, "bold"), command=self._start_generate
        )
        self.run_btn.pack(side=tk.LEFT, ipadx=10, ipady=4)

        self.log_box = scrolledtext.ScrolledText(bottom, height=6, state=tk.DISABLED, font=("Consolas", 8))
        self.log_box.pack(fill=tk.X, padx=6, pady=(0, 4))

    # ── 기능 메서드 ───────────────────────────────────────────────────────────

    def _add_scene(self):
        self.script_box.insert(tk.END, "\n" + SCENE_TEMPLATE)

    def _reset_script(self):
        if messagebox.askyesno("초기화", "스크립트를 기본값으로 초기화할까요?"):
            self.script_box.delete("1.0", tk.END)
            self.script_box.insert(tk.END, DEFAULT_SCRIPT)

    def _load_file(self):
        path = filedialog.askopenfilename(filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")])
        if path:
            with open(path, encoding="utf-8") as f:
                self.script_box.delete("1.0", tk.END)
                self.script_box.insert(tk.END, f.read())

    def _save_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.script_box.get("1.0", tk.END))

    def _refresh_preview(self):
        script = self.script_box.get("1.0", tk.END)
        try:
            scenes = parse_script(script)
        except Exception as e:
            messagebox.showerror("파싱 오류", str(e))
            return

        lines = []
        for s in scenes:
            lines.append(f"▶ 장면 {s.index}")
            lines.append(f"  자막    : {s.subtitle}")
            lines.append(f"  나레이션: {s.narration[:30]}{'...' if len(s.narration) > 30 else ''}")
            dur = f"{s.duration}초" if s.duration else "TTS 자동"
            lines.append(f"  길이    : {dur}")
            lines.append("")

        self.preview_box.config(state=tk.NORMAL)
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert(tk.END, "\n".join(lines) if lines else "장면 없음")
        self.preview_box.config(state=tk.DISABLED)

    def _log(self, msg: str):
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def _start_generate(self):
        script = self.script_box.get("1.0", tk.END)
        try:
            scenes = parse_script(script)
        except Exception as e:
            messagebox.showerror("파싱 오류", str(e))
            return

        if not scenes:
            messagebox.showwarning("경고", "장면이 없습니다. 스크립트를 확인하세요.")
            return

        output_name = self.output_var.get().strip() or "my_shorts.mp4"
        if not output_name.endswith(".mp4"):
            output_name += ".mp4"

        self.run_btn.config(state=tk.DISABLED)
        self.progress.start(12)
        self.status_var.set(f"영상 생성 중... ({len(scenes)}개 장면)")
        self._log(f"[시작] {len(scenes)}개 장면 → {output_name}")

        # 별도 스레드에서 실행 (UI 블로킹 방지)
        threading.Thread(
            target=self._generate_worker,
            args=(scenes, output_name),
            daemon=True
        ).start()

    def _generate_worker(self, scenes, output_name):
        # stdout을 로그 창으로 리다이렉트
        orig_stdout = sys.stdout
        sys.stdout = _LogRedirect(self._log)
        try:
            path = compose_video(scenes, output_name=output_name)
            self.after(0, self._on_done, path)
        except Exception as e:
            self.after(0, self._on_error, str(e))
        finally:
            sys.stdout = orig_stdout

    def _on_done(self, path: str):
        self.progress.stop()
        self.run_btn.config(state=tk.NORMAL)
        self.status_var.set(f"완료: {path}")
        self._log(f"[완료] {path}")
        messagebox.showinfo("완료", f"영상이 생성됐습니다!\n{path}")

    def _on_error(self, msg: str):
        self.progress.stop()
        self.run_btn.config(state=tk.NORMAL)
        self.status_var.set("오류 발생 — 로그 확인")
        self._log(f"[오류] {msg}")
        messagebox.showerror("오류", msg)


class _LogRedirect:
    """stdout을 GUI 로그 창으로 연결."""
    def __init__(self, log_fn):
        self._log = log_fn
        self._buf = ""

    def write(self, text):
        self._buf += text
        if "\n" in self._buf:
            lines = self._buf.split("\n")
            for line in lines[:-1]:
                if line.strip():
                    self._log(line)
            self._buf = lines[-1]

    def flush(self):
        pass


if __name__ == "__main__":
    app = ShortsApp()
    app.mainloop()
