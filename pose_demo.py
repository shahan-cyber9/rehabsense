"""Test script for PoseDetector."""

import cv2
from src.pose_detector import PoseDetector

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    detector = PoseDetector()

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # 1. Run AI detection
        result = detector.process(frame)
        
        # 2. Draw the skeleton
        frame = detector.draw(frame, result)

        cv2.imshow("RehabSense - Pose Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()