# RehabSense

Camera-based physiotherapy exercise monitoring and recovery-trend prototype.

## Problem
Home rehabilitation exercises are difficult to monitor objectively between supervised sessions.

## Proposed solution
RehabSense uses pose landmarks from an ordinary webcam and transparent joint-angle
geometry to estimate movement metrics such as repetitions, knee angle, angular
excursion, and session progress.

## Current status
Day 1: repository scaffold and environment setup. Core pipeline under development.

## Tech stack
- Python 3.14 (Windows)
- OpenCV via `opencv-contrib-python` 5.x (provides `cv2`)
- MediaPipe 1.1.x (pose landmarks)
- NumPy, Pandas
- Streamlit, Plotly
- pytest, Git/GitHub

## Environment notes
- MediaPipe 1.1.x is the version pinned in `requirements.txt`. If the legacy
  `mp.solutions.pose` interface is unavailable, `src/pose_detector.py` will use
  the MediaPipe Tasks `PoseLandmarker` API instead — the downstream geometry
  and exercise logic are unaffected.
- `opencv-contrib-python` is the `cv2` provider. Do **not** also install
  `opencv-python` in the same environment; the two packages conflict.

## Safety disclaimer
This is an engineering/research prototype only. It is not a diagnostic medical
device and must not be used for diagnosis, treatment decisions, or assessment of
rehabilitation readiness.