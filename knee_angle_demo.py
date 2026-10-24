"""Live knee angle demonstration with rep counting and session saving."""

import cv2
from src.pose_detector import PoseDetector
from src.geometry import calculate_angle
from src.exercise_analyzer import SquatAnalyzer
from src.session_store import save_session


def draw_hud(frame, text, position):
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.8
    thickness = 2
    
    (text_w, text_h), _ = cv2.getTextSize(text, font, scale, thickness)
    x, y = position
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (x - 10, y - text_h - 10), (x + text_w + 10, y + 10), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    cv2.putText(frame, text, (x, y), font, scale, (255, 255, 0), thickness, cv2.LINE_AA)


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    print("System ready. Stand side-on so I can see your knee.")
    detector = PoseDetector()
    analyzer = SquatAnalyzer()

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        result = detector.process(frame)
        
        if result.pose_landmarks:
            landmarks = result.pose_landmarks[0]
            h, w, _ = frame.shape

            l_hip = (landmarks[23].x, landmarks[23].y)
            l_knee = (landmarks[25].x, landmarks[25].y)
            l_ankle = (landmarks[27].x, landmarks[27].y)
            l_angle = calculate_angle(l_hip, l_knee, l_ankle)

            if l_angle is not None:
                analyzer.update(l_angle)
                
                summary = analyzer.get_summary()
                
                draw_hud(frame, f"REPS: {summary['reps']}", (30, 60))
                draw_hud(frame, f"STATE: {analyzer.stage.upper()}", (30, 120))
                draw_hud(frame, f"ANGLE: {int(l_angle)} DEG", (30, 180))
                
                r_hip = (landmarks[24].x, landmarks[24].y)
                r_knee = (landmarks[26].x, landmarks[26].y)
                r_ankle = (landmarks[28].x, landmarks[28].y)
                r_angle = calculate_angle(r_hip, r_knee, r_ankle)
                if r_angle is not None:
                    draw_hud(frame, f"R KNEE: {int(r_angle)} DEG", (w - 280, 60))

        frame = detector.draw(frame, result)
        cv2.imshow("RehabSense - Rep Counter", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("\n--- SESSION SUMMARY ---")
    final_stats = analyzer.get_summary()
    for key, value in final_stats.items():
        print(f"{key.upper()}: {value}")
    print("-----------------------")

# Save only if at least 1 rep was performed
    if final_stats["reps"] > 0:
        session_record = {
            "exercise": "squat",
            "reps": final_stats["reps"],
            "min_angle": final_stats["min_angle"],
            "max_angle": final_stats["max_angle"],
            "angular_excursion": final_stats["rom"]
        }
        save_session(session_record)
        print("Session saved successfully to data/sessions.csv")
    else:
        print("No reps performed. Session not saved.")


if __name__ == "__main__":
    main()