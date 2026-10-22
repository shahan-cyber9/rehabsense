"""P3.1 throwaway check: can the Pose Landmarker load and produce landmarks?"""

import cv2
import mediapipe as mp
import numpy as np

MODEL_PATH = "models/pose_landmarker_lite.task"

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_poses=1,
)

with PoseLandmarker.create_from_options(options) as landmarker:
    # Use a solid-gray dummy image — no person in it.
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)
    dummy[:] = (128, 128, 128)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=dummy)
    result = landmarker.detect(mp_image)

    print("Model loaded and detection ran.")
    print("Landmarks detected:", len(result.pose_landmarks))
    if result.pose_landmarks:
        print("Sample landmark 0 (x, y, visibility):",
              result.pose_landmarks[0][0].x,
              result.pose_landmarks[0][0].y,
              result.pose_landmarks[0][0].visibility)