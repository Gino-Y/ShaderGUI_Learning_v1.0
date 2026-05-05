from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

# 可靠定位 workspace 根目录：从本文件位置向上找包含 .git 或 CourseApp/ 的目录
SCRIPT_FILE = Path(__file__).resolve()
ROOT = SCRIPT_FILE.parent
for parent in [SCRIPT_FILE.parent, *SCRIPT_FILE.parents]:
    if (parent / ".git").exists() or (parent / "CourseApp" / "src").exists():
        ROOT = parent
        break

TRANSCRIPT_ROOT = ROOT / "CourseApp" / "public" / "transcripts"
SUBTITLE_ROOT = ROOT / "CourseApp" / "public" / "subtitles"
AUDIO_ROOT = ROOT / "CourseApp" / "public" / "audio"
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"


def clean_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    # 1. 移除代码块（```...```）
    text = re.sub(r"```[\s\S]*?```", " ", text)
    # 2. 移除行内代码（`...`）
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # 3. 移除标题符号（# ## ###）
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    # 4. 移除粗体/斜体符号（**bold** *italic*）
    text = re.sub(r"\*{1,2}([^\*]+)\*{1,2}", r"\1", text)
    text = re.sub(r"_{1,2}([^_]+)_{1,2}", r"\1", text)
    # 5. 移除链接/图片语法（[text](url) ![alt](url)）
    text = re.sub(r"!\[([^\]]*)\]\([^\)]*\)", r"\1", text)  # 图片
    text = re.sub(r"\[([^\]]*)\]\([^\)]*\)", r"\1", text)    # 链接
    # 6. 移除引用符号（>）
    text = re.sub(r"^\s*>+\s*", "", text, flags=re.MULTILINE)
    # 7. 移除水平线（--- *** ___）
    text = re.sub(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", "", text, flags=re.MULTILINE)
    # 8. 移除列表符号（- * 1.）
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    # 9. 移除表格语法（|）
    text = text.replace("|", " ")
    # 10. 移除内部指导字段（shotInstruction/focusInstruction/implementationHint/learnerTakeaway/Now focusing）
    text = re.sub(r"(shotInstruction|focusInstruction|implementationHint|learnerTakeaway|Now focusing)\s*[:：]\s*[^\n]*", "", text)
    # 11. 合并多余空白
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def transcript_to_sentences(path: Path) -> list[str]:
    text = clean_text(path)
    parts = [p.strip() for p in re.split(r"(?<=[。！？；.!?;])", text) if p.strip()]
    return parts or [text]


def write_subtitles(path: Path, out_path: Path) -> list[dict]:
    sentences = transcript_to_sentences(path)
    total_chars = max(1, sum(len(s) for s in sentences))
    duration = max(8.0, total_chars / 4.5)
    cursor = 0.0
    events = []
    for s in sentences:
        span = max(1.2, duration * (len(s) / total_chars))
        events.append({"start": round(cursor, 2), "end": round(cursor + span, 2), "text": s})
        cursor += span
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(events, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  Subtitle: {out_path.name} | {len(events)} segments | {cursor:.1f}s")
    return events


def write_audio(text_path: Path, out_path: Path, voice: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    clean_path = out_path.with_suffix(".txt")
    clean_path.write_text(clean_text(text_path), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "edge_tts", "--file", str(clean_path),
         "--voice", voice, "--rate", "+0%", "--pitch", "+0Hz",
         "--write-media", str(out_path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    clean_path.unlink(missing_ok=True)
    if result.returncode != 0 or not out_path.exists() or out_path.stat().st_size < 10_000:
        raise RuntimeError(result.stderr.strip() or "edge-tts failed")


def main() -> int:
    module = sys.argv[1] if len(sys.argv) > 1 else "Module_01"
    trans_dir = TRANSCRIPT_ROOT / module
    if not trans_dir.exists():
        print(f"[ERR] Transcript dir not found: {trans_dir}")
        return 1

    files = sorted(trans_dir.glob(f"{module}-p*-*.md"))
    if not files:
        print(f"[ERR] No transcript files found in {trans_dir}")
        return 1

    print(f"[generate_audio] Module: {module} | workspace: {ROOT}")
    for path in files:
        m = re.match(r".+-(p\d+)-.+\.md$", path.name)
        if not m:
            continue
        page = m.group(1)
        sub_out = SUBTITLE_ROOT / module / f"{page}.json"
        aud_out = AUDIO_ROOT / module / f"{page}.mp3"
        print(f"\nProcessing {path.name} ...")
        try:
            write_subtitles(path, sub_out)
            write_audio(path, aud_out, DEFAULT_VOICE)
            print(f"  Audio: {aud_out.name} | OK")
        except Exception as exc:
            print(f"  [ERR] {exc}")
            return 1

    print("\n✅ All done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
