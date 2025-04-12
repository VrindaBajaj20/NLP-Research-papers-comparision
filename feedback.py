import json
from pathlib import Path
import datetime 

class FeedbackDB:
    def __init__(self, path="feedback.json"):
        self.path = Path(path)
        self.data = self._load_data()

    def _load_data(self):
        if self.path.exists():
            with open(self.path, 'r') as f:
                return json.load(f)
        return {"papers": {}, "user_preferences": {}}

    def save_feedback(self, paper_id, rating, notes, user_id="anonymous"):
        if paper_id not in self.data["papers"]:
            self.data["papers"][paper_id] = []
        
        self.data["papers"][paper_id].append({
            "user": user_id,
            "rating": rating,
            "notes": notes,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # Update user preferences
        if user_id not in self.data["user_preferences"]:
            self.data["user_preferences"][user_id] = {"liked_keywords": []}
        
        self._save_data()

    def _save_data(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)