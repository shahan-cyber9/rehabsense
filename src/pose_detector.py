"""Pose landmark detection.

Day 3 will implement PoseDetector.

Implementation note for this environment:
MediaPipe 1.1.x is installed. If ``mediapipe.solutions.pose`` is not available,
use the MediaPipe Tasks ``PoseLandmarker`` API instead. Either way, this module
must return normalized landmark coordinates (x, y, visibility) for hip, knee,
and ankle so that ``src/geometry.py`` remains unchanged.
"""

# TODO (Day 3): implement PoseDetector.