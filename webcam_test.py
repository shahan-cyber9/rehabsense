"""Phase 2 webcam smoke test.

Opens the default camera, shows a live feed, and closes cleanly on 'q'.
No MediaPipe, no pose detection — only proves that OpenCV can access a camera.

Run:
    python webcam_test.py
"""

import cv2


def main() -> None:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError(
            "Could not open webcam. Check that:\n"
            "  1. Camera is connected and not used by another app (Teams/Zoom/browser).\n"
            "  2. Windows Settings > Privacy & security > Camera -> 'Camera access' is On.\n"
            "  3. Windows Settings > Privacy & security > Camera -> 'Let desktop apps access your camera' is On."
        )

    print("Camera opened. Press 'q' in the window to quit.")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Frame read failed — camera may have been disconnected.")
                break

            cv2.imshow("RehabSense - Webcam Test", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera released, windows closed.")


if __name__ == "__main__":
    main()