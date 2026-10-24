"""Live knee angle demonstration."""

import cv2
from src.pose_detector import PoseDetector
from src.geometry import calculate_angle


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    detector = PoseDetector()

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        result = detector.process(frame)
        
        if result.pose_landmarks:
            landmarks = result.pose_landmarks[0]
            h, w, _ = frame.shape

            hip = (landmarks[23].x, landmarks[23].y)
            knee = (landmarks[25].x, landmarks[25].y)
            ankle = (landmarks[27].x, landmarks[27].y)

            angle = calculate_angle(hip, knee, ankle)

            if angle is not None:
                knee_x, knee_y = int(knee[0] * w), int(knee[1] * h)
                
                cv2.putText(
                    frame,
                    f"{int(angle)} deg",
                    (knee_x + 20, knee_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

        frame = detector.draw(frame, result)
        cv2.imshow("RehabSense - Live Knee Angle", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()