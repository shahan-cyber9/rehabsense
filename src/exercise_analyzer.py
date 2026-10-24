"""Exercise state machine for repetition counting."""


class SquatAnalyzer:
    def __init__(self, down_threshold=100, up_threshold=160):
        self.down_threshold = down_threshold
        self.up_threshold = up_threshold
        
        self.stage = "up"
        self.reps = 0
        
        self.min_angle = 180.0
        self.max_angle = 0.0

    def update(self, angle):
        if angle is None:
            return

        self.min_angle = min(self.min_angle, angle)
        self.max_angle = max(self.max_angle, angle)

    # State Machine
        if angle < self.down_threshold and self.stage == "up":
            self.stage = "down"
            
        if angle > self.up_threshold and self.stage == "down":
            self.stage = "up"
            self.reps += 1

    def get_summary(self):
        return {
            "reps": self.reps,
            "min_angle": round(self.min_angle, 1) if self.min_angle < 180 else 0,
            "max_angle": round(self.max_angle, 1),
            "rom": round(self.max_angle - self.min_angle, 1) if self.max_angle > 0 else 0
        }