#!/usr/bin/env python3
"""Extract anonymized body and hand motion trajectories from a video segment."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np


POSE_EDGES = list(mp.solutions.pose.POSE_CONNECTIONS)
HAND_EDGES = list(mp.solutions.hands.HAND_CONNECTIONS)
JOINTS = {
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
}


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def landmarks_to_array(landmarks, count: int) -> np.ndarray:
    out = np.full((count, 4), np.nan, dtype=np.float32)
    if landmarks is None:
        return out
    for index, landmark in enumerate(landmarks.landmark[:count]):
        out[index] = (
            landmark.x,
            landmark.y,
            landmark.z,
            getattr(landmark, "visibility", 1.0),
        )
    return out


def interpolate_and_smooth(data: np.ndarray, max_gap: int, alpha: float) -> np.ndarray:
    """Interpolate short interior gaps, then apply a bidirectional EMA."""
    out = data.copy()
    frames, points, dimensions = out.shape
    timeline = np.arange(frames)
    for point in range(points):
        valid_indices = np.flatnonzero(np.isfinite(out[:, point, 0]))
        if not len(valid_indices):
            continue
        for dimension in range(dimensions):
            values = out[:, point, dimension]
            for start, end in zip(valid_indices[:-1], valid_indices[1:]):
                gap = end - start - 1
                if 0 < gap <= max_gap:
                    values[start + 1 : end] = np.interp(
                        timeline[start + 1 : end],
                        [start, end],
                        [values[start], values[end]],
                    )
        for dimension in range(3):
            values = out[:, point, dimension]
            forward = values.copy()
            last = np.nan
            for index, value in enumerate(values):
                if np.isfinite(value):
                    last = value if not np.isfinite(last) else alpha * value + (1 - alpha) * last
                    forward[index] = last
            backward = values.copy()
            last = np.nan
            for index in range(frames - 1, -1, -1):
                value = values[index]
                if np.isfinite(value):
                    last = value if not np.isfinite(last) else alpha * value + (1 - alpha) * last
                    backward[index] = last
            both = np.isfinite(forward) & np.isfinite(backward)
            values[both] = (forward[both] + backward[both]) / 2
            only_forward = np.isfinite(forward) & ~np.isfinite(backward)
            only_backward = np.isfinite(backward) & ~np.isfinite(forward)
            values[only_forward] = forward[only_forward]
            values[only_backward] = backward[only_backward]
    return out


def point_xy(array: np.ndarray, index: int, width: int, height: int):
    if index >= len(array) or not np.isfinite(array[index, 0]):
        return None
    return (
        int(np.clip(array[index, 0], 0, 1) * width),
        int(np.clip(array[index, 1], 0, 1) * height),
    )


def draw_graph(
    canvas,
    array,
    edges,
    color,
    line_width=3,
    radius=4,
    visibility_threshold=0.25,
):
    height, width = canvas.shape[:2]
    for start, end in edges:
        point_a = point_xy(array, start, width, height)
        point_b = point_xy(array, end, width, height)
        if point_a is None or point_b is None:
            continue
        low = array.shape[1] > 3 and (
            array[start, 3] < visibility_threshold or array[end, 3] < visibility_threshold
        )
        cv2.line(
            canvas,
            point_a,
            point_b,
            (92, 98, 108) if low else color,
            1 if low else line_width,
            cv2.LINE_AA,
        )
    for index in range(len(array)):
        point = point_xy(array, index, width, height)
        if point is None:
            continue
        low = array.shape[1] > 3 and array[index, 3] < visibility_threshold
        cv2.circle(
            canvas,
            point,
            max(2, radius - 1) if low else radius,
            (112, 118, 128) if low else (245, 245, 245),
            -1,
            cv2.LINE_AA,
        )
        cv2.circle(
            canvas,
            point,
            radius + 1,
            (92, 98, 108) if low else color,
            1,
            cv2.LINE_AA,
        )


def json_landmarks(array: np.ndarray):
    return [
        [None if not np.isfinite(value) else round(float(value), 6) for value in row]
        for row in array
    ]


def probe(path: Path) -> dict:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,duration,nb_frames",
            "-show_entries",
            "format=duration,size",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--duration", type=float)
    parser.add_argument("--no-overlay", action="store_true")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise SystemExit("ffmpeg and ffprobe must be available on PATH")
    source = args.input.expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"input not found: {source}")
    if args.start < 0 or (args.duration is not None and args.duration <= 0):
        raise SystemExit("start must be >= 0 and duration must be > 0")

    output = args.output.expanduser().resolve()
    data_dir, qc_dir, work_dir = output / "data", output / "qc", output / "work"
    for directory in (data_dir, qc_dir, work_dir):
        directory.mkdir(parents=True, exist_ok=True)

    source_probe = probe(source)
    with (qc_dir / "media-probe.json").open("w", encoding="utf-8") as handle:
        json.dump(source_probe, handle, ensure_ascii=False, indent=2)

    capture = cv2.VideoCapture(str(source))
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    source_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    start_frame = int(round(args.start * fps))
    end_frame = source_frames if args.duration is None else min(
        source_frames, start_frame + int(round(args.duration * fps))
    )
    if fps <= 0 or width <= 0 or height <= 0:
        raise SystemExit("unable to read source dimensions or frame rate")
    if start_frame >= source_frames or end_frame <= start_frame:
        raise SystemExit("requested range is outside the video")
    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    pose_raw, left_raw, right_raw = [], [], []
    holistic = mp.solutions.holistic.Holistic(
        static_image_mode=False,
        model_complexity=2,
        smooth_landmarks=True,
        enable_segmentation=False,
        refine_face_landmarks=False,
        min_detection_confidence=0.45,
        min_tracking_confidence=0.45,
    )
    for _ in range(end_frame - start_frame):
        ok, frame = capture.read()
        if not ok:
            break
        result = holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        pose_raw.append(landmarks_to_array(result.pose_landmarks, 33))
        left_raw.append(landmarks_to_array(result.left_hand_landmarks, 21))
        right_raw.append(landmarks_to_array(result.right_hand_landmarks, 21))
    holistic.close()
    capture.release()
    if not pose_raw:
        raise SystemExit("no frames were decoded")

    pose_raw = np.stack(pose_raw)
    left_raw = np.stack(left_raw)
    right_raw = np.stack(right_raw)
    pose = interpolate_and_smooth(pose_raw, max_gap=12, alpha=0.48)
    left = interpolate_and_smooth(left_raw, max_gap=8, alpha=0.55)
    right = interpolate_and_smooth(right_raw, max_gap=8, alpha=0.55)
    processed = len(pose)

    np.savez_compressed(
        data_dir / "motion-keypoints.npz",
        pose_raw=pose_raw,
        left_hand_raw=left_raw,
        right_hand_raw=right_raw,
        pose_smooth=pose,
        left_hand_smooth=left,
        right_hand_smooth=right,
        fps=np.array([fps]),
        width=np.array([width]),
        height=np.array([height]),
        source_start_frame=np.array([start_frame]),
    )

    pose_detected = np.isfinite(pose_raw[:, :, 0]).any(axis=1)
    left_detected = np.isfinite(left_raw[:, :, 0]).any(axis=1)
    right_detected = np.isfinite(right_raw[:, :, 0]).any(axis=1)
    payload = {
        "schema": "rnskill.human-motion.landmarks.v1",
        "source": str(source),
        "source_sha256": sha256(source),
        "coordinate_space": "normalized_image_xy_and_relative_z",
        "fps": fps,
        "width": width,
        "height": height,
        "source_start_frame": start_frame,
        "source_start_seconds": start_frame / fps,
        "frame_count": processed,
        "smoothing": {
            "method": "bidirectional_ema",
            "pose_alpha": 0.48,
            "hand_alpha": 0.55,
            "max_pose_gap": 12,
            "max_hand_gap": 8,
        },
        "frames": [
            {
                "frame": index,
                "source_frame": start_frame + index,
                "time_seconds": round(index / fps, 6),
                "source_time_seconds": round((start_frame + index) / fps, 6),
                "pose": json_landmarks(pose[index]),
                "left_hand": json_landmarks(left[index]),
                "right_hand": json_landmarks(right[index]),
                "detected": {
                    "pose": bool(pose_detected[index]),
                    "left_hand": bool(left_detected[index]),
                    "right_hand": bool(right_detected[index]),
                },
            }
            for index in range(processed)
        ],
    }
    json_path = data_dir / "motion-keypoints.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))

    joint_confidence = {}
    for name, index in JOINTS.items():
        visibility = pose_raw[:, index, 3]
        joint_confidence[name] = {
            "mean_visibility": round(float(np.nanmean(visibility)), 4),
            "coverage_gte_0_25": round(float(np.nanmean(visibility >= 0.25)), 4),
            "coverage_gte_0_50": round(float(np.nanmean(visibility >= 0.50)), 4),
        }
    stats = {
        "source_frames": source_frames,
        "source_start_frame": start_frame,
        "requested_end_frame_exclusive": end_frame,
        "frames_processed": processed,
        "fps": fps,
        "duration_seconds": round(processed / fps, 6),
        "pose_coverage": round(float(pose_detected.mean()), 4),
        "left_hand_coverage": round(float(left_detected.mean()), 4),
        "right_hand_coverage": round(float(right_detected.mean()), 4),
        "joint_confidence": joint_confidence,
        "warning": "Hand coverage is raw detector coverage; smoothing does not prove hidden finger motion.",
    }
    with (qc_dir / "extraction-stats.json").open("w", encoding="utf-8") as handle:
        json.dump(stats, handle, ensure_ascii=False, indent=2)

    overlay_intermediate = work_dir / "overlay-intermediate.mp4"
    skeleton_intermediate = work_dir / "skeleton-intermediate.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    overlay_writer = None if args.no_overlay else cv2.VideoWriter(
        str(overlay_intermediate), fourcc, fps, (width, height)
    )
    skeleton_writer = cv2.VideoWriter(
        str(skeleton_intermediate), fourcc, fps, (width, height)
    )
    capture = cv2.VideoCapture(str(source))
    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    for index in range(processed):
        ok, frame = capture.read()
        if not ok:
            raise SystemExit(f"render pass stopped at frame {index}")
        canvases = [np.full_like(frame, (24, 27, 34))]
        if overlay_writer is not None:
            canvases.append(frame.copy())
        for canvas in canvases:
            draw_graph(canvas, pose[index], POSE_EDGES, (40, 210, 255), 3, 3)
            draw_graph(canvas, left[index], HAND_EDGES, (255, 150, 55), 2, 2, 0)
            draw_graph(canvas, right[index], HAND_EDGES, (105, 90, 255), 2, 2, 0)
            cv2.putText(
                canvas,
                f"frame {index:04d}  {index / fps:06.2f}s",
                (24, 42),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (245, 245, 245),
                2,
                cv2.LINE_AA,
            )
        skeleton_writer.write(canvases[0])
        if overlay_writer is not None:
            overlay_writer.write(canvases[1])
    capture.release()
    skeleton_writer.release()
    if overlay_writer is not None:
        overlay_writer.release()

    skeleton_path = qc_dir / "motion-skeleton.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(skeleton_intermediate),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(skeleton_path),
        ]
    )
    contact_path = qc_dir / "contact-sheet.jpg"
    sample_count = min(6, processed)
    sample_frames = np.linspace(0, processed - 1, sample_count, dtype=int)
    select = "+".join(f"eq(n\\,{frame})" for frame in sample_frames)
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(skeleton_path),
            "-vf",
            f"select='{select}',scale=640:360,tile=3x2",
            "-frames:v",
            "1",
            str(contact_path),
        ]
    )
    if overlay_writer is not None:
        overlay_path = qc_dir / "motion-overlay.mp4"
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(overlay_intermediate),
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(overlay_path),
            ]
        )

    print(
        json.dumps(
            {
                "output": str(output),
                "stats": stats,
                "keypoints_sha256": sha256(json_path),
                "skeleton_sha256": sha256(skeleton_path),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
