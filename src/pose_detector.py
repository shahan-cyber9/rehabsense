"""Pose landmark detection using MediaPipe Tasks API."""

import cv2
import mediapipe as mp


class PoseDetector:
    def __init__(self, model_path="models/pose_landmarker_lite.task"):
        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO,
            num_poses=1,
        )
        
        self.landmarker = PoseLandmarker.create_from_options(options)
        self.timestamp_ms = 0

    def process(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        self.timestamp_ms += 33
        result = self.landmarker.detect_for_video(mp_image, self.timestamp_ms)
        return result

    def draw(self, frame, result):
        if result.pose_landmarks:
            h, w, _ = frame.shape
            landmarks = result.pose_landmarks[0]
            
            joints = [23, 24, 25, 26, 27, 28]
            for idx in joints:
                lm = landmarks[idx]
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 6, (0, 255, 0), -1)
                
            self._draw_line(frame, landmarks, 23, 25, w, h)
            self._draw_line(frame, landmarks, 25, 27, w, h)
            self._draw_line(frame, landmarks, 24, 26, w, h)
            self._draw_line(frame, landmarks, 26, 28, w, h)
            
        return frame

    def _draw_line(self, frame, landmarks, idx1, idx2, w, h):
        lm1 = landmarks[idx1]
        lm2 = landmarks[idx2]
        x1, y1 = int(lm1.x * w), int(lm1.y * h)
        x2, y2 = int(lm2.x * w), int(lm2.y * h)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)