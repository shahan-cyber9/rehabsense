"""Pose landmark detection using MediaPipe Tasks API.

Phase 3 (Vision & Geometry) - P3.2 implementation.
"""

import cv2
import mediapipe as mp


class PoseDetector:
    def __init__(self, model_path="models/pose_landmarker_lite.task"):
        # Setup MediaPipe Tasks API
        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO,
            num_poses=1,
        )
        
        # Initialize the model
        self.landmarker = PoseLandmarker.create_from_options(options)
        self.timestamp_ms = 0

    def process(self, frame):
        """Takes a BGR frame, runs pose detection, returns the result."""
        # 1. Convert OpenCV BGR to MediaPipe RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 2. Wrap it in a MediaPipe Image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # 3. Increment timestamp (must be strictly increasing for VIDEO mode)
        self.timestamp_ms += 33
        
        # 4. Run detection
        result = self.landmarker.detect_for_video(mp_image, self.timestamp_ms)
        return result

    def draw(self, frame, result):
        """Draws the hip, knee, and ankle landmarks and lines on the frame."""
        if result.pose_landmarks:
            h, w, _ = frame.shape
            landmarks = result.pose_landmarks[0]
            
            # MediaPipe BlazePose indices: 23=L_Hip, 24=R_Hip, 25=L_Knee, 26=R_Knee, 27=L_Ankle, 28=R_Ankle
            joints = [23, 24, 25, 26, 27, 28]
            
            # Draw the joints (green dots)
            for idx in joints:
                lm = landmarks[idx]
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 6, (0, 255, 0), -1)
                
            # Draw the bones (blue lines)
            self._draw_line(frame, landmarks, 23, 25, w, h)  # Left hip -> Left knee
            self._draw_line(frame, landmarks, 25, 27, w, h)  # Left knee -> Left ankle
            self._draw_line(frame, landmarks, 24, 26, w, h)  # Right hip -> Right knee
            self._draw_line(frame, landmarks, 26, 28, w, h)  # Right knee -> Right ankle
            
        return frame

    def _draw_line(self, frame, landmarks, idx1, idx2, w, h):
        lm1 = landmarks[idx1]
        lm2 = landmarks[idx2]
        x1, y1 = int(lm1.x * w), int(lm1.y * h)
        x2, y2 = int(lm2.x * w), int(lm2.y * h)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)