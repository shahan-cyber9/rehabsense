# RehabSense Architecture

## Pipeline
1. **Camera Capture**: OpenCV captures live frames.
2. **Pose Estimation**: MediaPipe Tasks API extracts 33 3D body landmarks.
3. **Quality Gate**: Rejects frames with low visibility or invalid posture.
4. **Geometry**: Calculates joint angles using dot-product mathematics.
5. **State Machine**: Counts reps based on movement phases.
6. **Persistence**: Saves session metrics to `data/sessions.csv`.
7. **Dashboard**: Reads the CSV to display KPIs and progress charts.

## Design Principle
The MVP favors transparent, interpretable measurements over black-box medical predictions.