import random
from datetime import datetime


class ActivityGenerator:
    def __init__(self):
        self.activities = [
            "coding a machine learning model",
            "reading about quantum computing",
            "sketching something badly in my notebook",
            "at a cozy cafe drinking coffee",
            "just came back from a techno party",
            "debugging some annoying code",
            "scrolling through random research papers",
            "watching the sunset from my window",
            "trying to cook something experimental",
        ]

    def get_activity(self):
        current_hour = datetime.now().hour

        # simple time-based context
        if 6 <= current_hour < 12:
            time_context = "morning"
        elif 12 <= current_hour < 18:
            time_context = "afternoon"
        elif 18 <= current_hour < 23:
            time_context = "evening"
        else:
            time_context = "late night"

        activity = random.choice(self.activities)

        return f"It's {time_context}, and I'm currently {activity}."