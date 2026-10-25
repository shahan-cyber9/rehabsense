"""Live bicep curl demonstration tracking both arms with posture validation."""

import cv2
from collections import deque
from src.pose_detector import PoseDetector
from src.geometry import calculate_angle
from src.exercise_analyzer import BicepAnalyzer
from src.session_store import save_session
from knee_angle_demo import draw_hud


def is_valid_posture(shoulder, elbow):
    # 1. Elbow must be lower than the shoulder (Y increases downwards in OpenCV)
    if elbow.y < shoulder.y:
        return False
    
    # 2. Upper arm shouldn't be sticking out horizontally
    if abs(shoulder.x - elbow.x) > abs(shoulder.y - elbow.y) * 1.2:
        return False
        
    return True


def get_smoothed_angle(landmarks, idx_a, idx_b, idx_c, angle_buffer):
    if (landmarks[idx_a].visibility < 0.5 or 
        landmarks[idx_b].visibility < 0.5 or 
        landmarks[idx_c].visibility < 0.5):
        return None

    shoulder = landmarks[idx_a]
    elbow = landmarks[idx_b]
    
    if not is_valid_posture(shoulder, elbow):
        return None

    a = (shoulder.x, shoulder.y)
    b = (elbow.x, elbow.y)
    c = (landmarks[idx_c].x, landmarks[idx_c].y)
    
    raw_angle = calculate_angle(a, b, c)
    
    if raw_angle is None:
        return None

    if raw_angle < 10.0 or raw_angle > 185.0:
        return None

    angle_buffer.append(raw_angle)
    smoothed_angle = sum(angle_buffer) / len(angle_buffer)
    
    return smoothed_angle


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    print("System ready. Face side-on. Tracking both arms automatically.")
    detector = PoseDetector()
    
    l_analyzer = BicepAnalyzer()
    r_analyzer = BicepAnalyzer()
    
    l_buffer = deque(maxlen=5)
    r_buffer = deque(maxlen=5)

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        result = detector.process(frame)
        
        if result.pose_landmarks:
            landmarks = result.pose_landmarks[0]
            h, w, _ = frame.shape

            # Left Arm
            l_angle = get_smoothed_angle(landmarks, 11, 13, 15, l_buffer)
            if l_angle is not None:
                l_analyzer.update(l_angle)
                l_summary = l_analyzer.get_summary()
                draw_hud(frame, f"L REPS: {l_summary['reps']}", (30, 60))
                draw_hud(frame, f"L ANGLE: {int(l_angle)}", (30, 120))
            else:
                # Show that posture is invalid so the user knows to fix it
                draw_hud(frame, "L POSTURE: INVALID", (30, 120), color=(0, 0, 255))

            # Right Arm
            r_angle = get_smoothed_angle(landmarks, 12, 14, 16, r_buffer)
            if r_angle is not None:
                r_analyzer.update(r_angle)
                r_summary = r_analyzer.get_summary()
                draw_hud(frame, f"R REPS: {r_summary['reps']}", (w - 220, 60))
                draw_hud(frame, f"R ANGLE: {int(r_angle)}", (w - 220, 120))
            else:
                draw_hud(frame, "R POSTURE: INVALID", (w - 220, 120), color=(0, 0, 255))

        frame = detector.draw(frame, result)
        cv2.imshow("RehabSense - Bicep Curls", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("\n--- SESSION SUMMARY ---")
    
    l_stats = l_analyzer.get_summary()
    if l_stats["reps"] > 0:
        save_session({
            "exercise": "bicep_curl_L",
            "reps": l_stats["reps"],
            "min_angle": l_stats["min_angle"],
            "max_angle": l_stats["max_angle"],
            "angular_excursion": l_stats["rom"]
        })
        print(f"Left Arm: {l_stats['reps']} reps saved.")
    
    r_stats = r_analyzer.get_summary()
    if r_stats["reps"] > 0:
        save_session({
            "exercise": "bicep_curl_R",
            "reps": r_stats["reps"],
            "min_angle": r_stats["min_angle"],
            "max_angle": r_stats["max_angle"],
            "angular_excursion": r_stats["rom"]
        })
        print(f"Right Arm: {r_stats['reps']} reps saved.")


if __name__ == "__main__":
    main()