# RehabSense

A Camera-based physiotherapy exercise monitoring and recovery-trend prototype.

## Problem
Home rehabilitation exercises are difficult to monitor objectively between supervised sessions. Patients often perform exercises with poor form or incorrect volume, and clinicians lack quantitative data on adherence and progress.

## Proposed Solution
RehabSense uses an ordinary webcam to estimate pose landmarks during selected knee and arm rehabilitation exercises. It converts body landmarks into interpretable joint-angle metrics, counts repetitions using a state machine, and visualizes longitudinal recovery progress. 

## Key Features
- **Real-time Pose Estimation:** Uses MediaPipe Tasks API to track body landmarks.
- **Biomechanical Posture Validation:** Rejects invalid movements and occluded limbs.
- **State Machine Rep Counting:** Accurately counts reps with temporal smoothing to reduce AI jitter.
- **Clinical Dashboard:** Streamlit-based UI to track range of motion (ROM) over time.
- **Data Persistence:** Saves session metrics locally to a CSV.

## Tech Stack
Python 3.14, OpenCV, MediaPipe, Pandas, Streamlit, Plotly, pytest.

## How to Run Locally
1. Clone the repository:
   git clone https://github.com/shahan-cyber9/rehabsense.git
   cd rehabsense
2. Create and activate a virtual environment:
   python -m venv .venv
   .\.venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Download the MediaPipe model (`pose_landmarker_lite.task`) and place it in a `models/` folder.
5. Run the app:
   streamlit run app.py

## Visuals
### Live Pose Tracking
![Pose Demo](assets/screenshots/pose_demo.png)

### Clinical Dashboard
![Dashboard](assets/screenshots/dashboard.png)

## Safety Disclaimer
This is an engineering/research prototype only. It is not a diagnostic medical device and must not be used for diagnosis, treatment decisions, or assessment of rehabilitation readiness.