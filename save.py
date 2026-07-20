
import json
import os
from datetime import datetime

class SaveManager:
    def __init__(self):
        self.save_dir = "save"
        self.save_file = f"{self.save_dir}/game_data.json"
        self.backup_file = f"{self.save_dir}/game_data_backup.json"
        self.data = self.load()
        
    def load(self):
        try:
            os.makedirs(self.save_dir, exist_ok=True)
            with open(self.save_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.create_default_save()
    
    def create_default_save(self):
        return {
            "high_score": 0,
            "total_coins": 0,
            "total_games": 0,
            "total_distance": 0,
            "unlocked_outfits": [0],
            "current_outfit": 0,
            "unlocked_shoes": [0],
            "current_shoes": 0,
            "unlocked_hairstyles": [0],
            "current_hairstyle": 0,
            "unlocked_accessories": [0],
            "current_accessories": 0,
            "settings": {
                "music_volume": 0.7,
                "sfx_volume": 0.7,
                "music_on": True,
                "sfx_on": True
            },
            "achievements": {},
            "last_played": None,
            "total_play_time": 0
        }
    
    def save(self, data=None):
        if data:
            self.data.update(data)

        self.data["last_played"] = datetime.now().isoformat()
        if "total_play_time" in self.data:
            self.data["total_play_time"] += 1  
        
        try:
            os.makedirs(self.save_dir, exist_ok=True)
            with open(self.save_file, "w") as f:
                json.dump(self.data, f, indent=2)
            with open(self.backup_file, "w") as f:
                json.dump(self.data, f, indent=2)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
    
    def load_backup(self):
        try:
            with open(self.backup_file, "r") as f:
                return json.load(f)
        except:
            return None
    
    def reset(self):
        self.data = self.create_default_save()
        self.save()
        return True
    
    def get_high_score(self):
        return self.data.get("high_score", 0)
    
    def set_high_score(self, score):
        if score > self.data.get("high_score", 0):
            self.data["high_score"] = score
            self.save()
            return True
        return False
    
    def add_coins(self, amount):
        self.data["total_coins"] = self.data.get("total_coins", 0) + amount
        self.save()
    
    def unlock_outfit(self, outfit_id):
        if "unlocked_outfits" not in self.data:
            self.data["unlocked_outfits"] = []
        if outfit_id not in self.data["unlocked_outfits"]:
            self.data["unlocked_outfits"].append(outfit_id)
            self.save()
            return True
        return False
    
    def set_current_outfit(self, outfit_id):
        if outfit_id in self.data.get("unlocked_outfits", []):
            self.data["current_outfit"] = outfit_id
            self.save()
            return True
        return False

class SettingsManager:
    def __init__(self):
        self.settings_file = "save/settings.json"
        self.load()
    
    def load(self):
        try:
            with open(self.settings_file, "r") as f:
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = self.create_default_settings()
            self.save()
    
    def create_default_settings(self):
        return {
            "music_volume": 0.7,
            "sfx_volume": 0.7,
            "music_on": True,
            "sfx_on": True,
            "screen_width": 1200,
            "screen_height": 700,
            "fullscreen": False,
            "particles": True,
            "fps_counter": False
        }
    
    def save(self):
        try:
            os.makedirs("save", exist_ok=True)
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def set(self, key, value):
        self.settings[key] = value
        self.save()