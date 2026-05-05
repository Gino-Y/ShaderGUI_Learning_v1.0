from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TRANSCRIPT_ROOT = ROOT / "CourseApp" / "public" / "transcripts"
SUBTITLE_ROOT = ROOT / "CourseApp" / "public" / "subtitles"
AUDIO_ROOT = ROOT / "CourseApp" / "public" / "audio"
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"

def clean_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def transcript_to_sentences(path: Path) -> list[str]:
    text = clean_text(path)
    parts = [part.strip() for part in re.split(r"(?<=[。！？；.!?;])", text) if part.strip()]
    return parts or [text]

def write_subtitles(path: Path, out_path: Path) -> None:
    sentences = transcript_to_sentences(path)
    total_chars = max(1, sum(len(item) for item in sentences))
    duration = max(8.0, total_chars / 5.2)
    cursor = 0.0
    events = []
    for sentence in sentences:
        span = max(1.2, duration * (len(sentence) / total_chars))
        events.append({"start": round(cursor, 2), "end": round(cursor + span, 2), "text": sentence})
        cursor += span
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")

def write_edge_tts_mp3(text_path: Path, out_path: Path, voice: str, rate: str, pitch: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    clean_path = out_path.with_suffix(".txt")
    clean_path.write_text(clean_text(text_path), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "edge_tts",
            "--file",
            str(clean_path),
            "--voice",
            voice,
            "--rate",
            rate,
            "--pitch",
            pitch,
            "--write-media",
            str(out_path),
        ],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    clean_path.unlink(missing_ok=True)
    if result.returncode != 0 or not out_path.exists() or out_path.stat().st_size < 10_000:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"edge-tts failed: {out_path}")

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate high-quality narration mp3 and subtitle JSON from transcripts.")
    parser.add_argument("module")
    parser.add_argument("--voice", default=DEFAULT_VOICE)
    parser.add_argument("--rate", default="+0%")
    parser.add_argument("--pitch", default="+0Hz")
    args = parser.parse_args()
    module = args.module
    files = sorted((TRANSCRIPT_ROOT / module).glob(f"{module}-p*-*.md"))
    if not files:
        print(f"no transcripts for {module}", file=sys.stderr)
        return 1
    for path in files:
        match = re.match(r".+-(p\d+)-.+\.md$", path.name)
        if not match:
            continue
        page = match.group(1)
        write_subtitles(path, SUBTITLE_ROOT / module / f"{page}.json")
        write_edge_tts_mp3(path, AUDIO_ROOT / module / f"{page}.mp3", args.voice, args.rate, args.pitch)
        print(f"generated high-quality audio/subtitles {module}/{page}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
