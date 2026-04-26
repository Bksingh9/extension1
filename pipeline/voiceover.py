"""Voice-over pipeline for The Dossier.

Parses an episode's script.md, synthesises one WAV per scene, concatenates
them, generates an SRT file, and muxes audio + subtitles onto the rendered
video.

TTS service selection — set DOSSIER_TTS env var:
    DOSSIER_TTS=espeak   (default — local, no network, robotic but works)
    DOSSIER_TTS=piper    (best free quality; needs an .onnx voice file)

Piper voice models live at huggingface.co/rhasspy/piper-voices. Download
e.g. en_US-amy-medium.onnx + .json and pass the .onnx path via
DOSSIER_PIPER_VOICE=/abs/path/to/voice.onnx.

CLI:
    python pipeline/voiceover.py episodes/001-pilot

Outputs to episodes/<slug>/render/:
    voiceover.wav            single concatenated audio track
    preview-full-qk-vo.mp4   4K video muxed with VO
    subtitles.srt            scene-by-scene subtitle file
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SCENE_MARKER = re.compile(
    r"^\[SCENE\s+(\d+)\s+—\s+(\w+)\s+—\s+(\d+):(\d{2})–(\d+):(\d{2})\]\s*$"
)


@dataclass
class Scene:
    number: int
    name: str
    start_s: float
    end_s: float
    text: str

    @property
    def duration(self) -> float:
        return self.end_s - self.start_s


def parse_script(script_path: Path) -> list[Scene]:
    """Extract per-scene (number, name, start, end, text) from script.md."""
    lines = script_path.read_text().splitlines()
    scenes: list[Scene] = []
    current: dict | None = None
    text_buf: list[str] = []

    def flush() -> None:
        if current is None:
            return
        text = " ".join(l.strip() for l in text_buf if l.strip())
        # Strip stage directions like *(scaffold)*.
        text = re.sub(r"\*\([^)]*\)\*", "", text).strip()
        if text:
            scenes.append(Scene(
                number=current["n"],
                name=current["name"],
                start_s=current["start"],
                end_s=current["end"],
                text=text,
            ))

    for line in lines:
        m = SCENE_MARKER.match(line)
        if m:
            flush()
            n, name, sm, ss, em, es = m.groups()
            current = {
                "n": int(n),
                "name": name,
                "start": int(sm) * 60 + int(ss),
                "end": int(em) * 60 + int(es),
            }
            text_buf = []
        elif current is not None:
            # End current scene on any markdown heading — that's the post-script
            # footer (word count check, post-script checklist, etc).
            if line.startswith("##") or line.startswith("# "):
                flush()
                current = None
                continue
            # Skip horizontal rules.
            if line.startswith("---"):
                continue
            text_buf.append(line)
    flush()
    return scenes


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def synth_espeak(text: str, target_seconds: float, out_wav: Path) -> None:
    """eSpeak NG synth tuned to fit `target_seconds`. Robotic but offline."""
    n = max(words(text), 1)
    # WPM that should land near the target. Clamp to listenable range.
    wpm = int(n / max(target_seconds, 1.0) * 60)
    wpm = max(120, min(wpm, 200))
    subprocess.run(
        [
            "espeak-ng",
            "-v", "en-us",
            "-s", str(wpm),
            "-p", "30",          # pitch a touch lower than default
            "-w", str(out_wav),
            text,
        ],
        check=True,
    )


def synth_piper(text: str, target_seconds: float, out_wav: Path) -> None:
    """Piper synth — needs an .onnx voice file via DOSSIER_PIPER_VOICE."""
    voice = os.environ.get("DOSSIER_PIPER_VOICE")
    if not voice or not Path(voice).exists():
        raise RuntimeError(
            "Set DOSSIER_PIPER_VOICE=/path/to/voice.onnx (download from "
            "huggingface.co/rhasspy/piper-voices)."
        )
    n = max(words(text), 1)
    natural_seconds = n / 150 * 60  # piper's natural pace ≈ 150 wpm
    length_scale = max(0.7, min(target_seconds / natural_seconds, 1.4))
    subprocess.run(
        [
            "piper",
            "-m", voice,
            "--length-scale", f"{length_scale:.3f}",
            "-f", str(out_wav),
        ],
        input=text,
        text=True,
        check=True,
    )


def synth(text: str, target_seconds: float, out_wav: Path) -> None:
    service = os.environ.get("DOSSIER_TTS", "espeak").lower()
    if service == "piper":
        synth_piper(text, target_seconds, out_wav)
    else:
        synth_espeak(text, target_seconds, out_wav)


def _atempo_chain(factor: float) -> str:
    """Chain atempo filters since each only accepts 0.5..2.0."""
    chain = []
    while factor > 2.0:
        chain.append("atempo=2.0")
        factor /= 2.0
    while factor < 0.5:
        chain.append("atempo=0.5")
        factor /= 0.5
    chain.append(f"atempo={factor:.4f}")
    return ",".join(chain)


def pad_to_duration(in_wav: Path, target_seconds: float, out_wav: Path) -> None:
    """Land on target_seconds exactly: pad with silence if short, time-stretch
    if long. Time-stretch uses ffmpeg's atempo (preserves pitch).
    """
    duration = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(in_wav)]
    ).strip())
    if abs(duration - target_seconds) < 0.05:
        shutil.copy(in_wav, out_wav)
        return
    if duration < target_seconds:
        pad = target_seconds - duration
        af = f"apad=pad_dur={pad:.3f}"
    else:
        # Speed up the audio to fit. atempo factor = original / target.
        factor = duration / target_seconds
        af = _atempo_chain(factor)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(in_wav),
         "-af", af,
         "-t", f"{target_seconds:.3f}",
         "-acodec", "pcm_s16le", "-ar", "22050", "-ac", "1",
         str(out_wav)],
        check=True, capture_output=True,
    )


def concat_wavs(wavs: list[Path], out_wav: Path) -> None:
    list_file = out_wav.parent / "_concat.txt"
    list_file.write_text("\n".join(f"file '{w.resolve()}'" for w in wavs) + "\n")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", str(list_file), "-c", "copy", str(out_wav)],
        check=True, capture_output=True,
    )
    list_file.unlink()


def mux(video_path: Path, audio_path: Path, out_path: Path,
        srt_path: Path | None = None) -> None:
    cmd = ["ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_path)]
    if srt_path is not None:
        # Burn-in soft subs (mov_text) so YouTube reads them automatically.
        cmd += ["-i", str(srt_path)]
    cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k"]
    if srt_path is not None:
        cmd += ["-c:s", "mov_text", "-metadata:s:s:0", "language=eng"]
    cmd += ["-shortest", str(out_path)]
    subprocess.run(cmd, check=True, capture_output=True)


def write_srt(scenes: list[Scene], out_path: Path) -> None:
    """One SRT entry per scene, using scene markers as timing source."""
    def fmt(t: float) -> str:
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int((t - int(t)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    chunks: list[str] = []
    for i, scene in enumerate(scenes, 1):
        chunks.append(f"{i}\n{fmt(scene.start_s)} --> {fmt(scene.end_s)}\n{scene.text}\n")
    out_path.write_text("\n".join(chunks))


def actual_scene_duration(episode_dir: Path, scene_name: str) -> float | None:
    """Look up the actual rendered duration of a scene's 4K mp4."""
    candidate = episode_dir / "media" / "videos" / "scene" / "2160p60" / f"{scene_name}.mp4"
    if not candidate.exists():
        return None
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(candidate)]
    ).strip())


def build(episode_dir: Path) -> None:
    script = episode_dir / "script.md"
    video = episode_dir / "render" / "preview-full-qk.mp4"
    if not script.exists():
        sys.exit(f"missing {script}")
    if not video.exists():
        sys.exit(f"missing {video} — render the 4K pilot first")

    out_dir = episode_dir / "render"
    work = out_dir / "_vo"
    work.mkdir(parents=True, exist_ok=True)

    scenes = parse_script(script)
    print(f"Parsed {len(scenes)} scenes from {script}.")

    # Per-scene synth + pad/stretch to the ACTUAL rendered scene duration
    # (script.md durations are nominal targets; renders drift slightly).
    padded_wavs: list[Path] = []
    srt_running_t = 0.0
    srt_scenes: list[Scene] = []
    for scene in scenes:
        actual = actual_scene_duration(episode_dir, scene.name)
        target = actual if actual else scene.duration
        raw = work / f"scene-{scene.number:02d}-{scene.name}-raw.wav"
        padded = work / f"scene-{scene.number:02d}-{scene.name}.wav"
        synth(scene.text, target, raw)
        pad_to_duration(raw, target, padded)
        padded_wavs.append(padded)
        print(f"  scene {scene.number:02d} {scene.name:<10s} script {scene.duration:5.1f}s  "
              f"render {target:5.1f}s  ({words(scene.text)} words)")
        srt_scenes.append(Scene(scene.number, scene.name,
                                srt_running_t, srt_running_t + target, scene.text))
        srt_running_t += target

    voiceover = out_dir / "voiceover.wav"
    concat_wavs(padded_wavs, voiceover)
    print(f"Wrote {voiceover}.")

    srt = out_dir / "subtitles.srt"
    write_srt(srt_scenes, srt)
    print(f"Wrote {srt} (timed against actual render).")

    final = out_dir / "preview-full-qk-vo.mp4"
    mux(video, voiceover, final, srt_path=srt)
    print(f"Wrote {final}.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python pipeline/voiceover.py <episode_dir>")
    build(Path(sys.argv[1]))
