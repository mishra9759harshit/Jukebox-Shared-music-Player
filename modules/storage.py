import json
import os

class Storage:
    def __init__(self, playlist_file="playlist.json", settings_file="settings.json"):
        self.playlist_file = playlist_file  # File for storing playlist
        self.settings_file = settings_file  # File for storing settings

    def save_playlist(self, playlist):
        """Save the current playlist to a JSON file."""
        try:
            with open(self.playlist_file, "w") as f:
                json.dump(playlist, f, indent=4)
            print("Playlist saved successfully.")
        except Exception as e:
            print(f"Error saving playlist: {e}")

    def load_playlist(self):
        """Load the playlist from a JSON file."""
        if os.path.exists(self.playlist_file):
            try:
                with open(self.playlist_file, "r") as f:
                    playlist = json.load(f)
                return playlist
            except Exception as e:
                print(f"Error loading playlist: {e}")
        return []  # Return empty list if no playlist file is found

    def save_settings(self, settings):
        """Save user settings to a JSON file."""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(settings, f, indent=4)
            print("Settings saved successfully.")
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_settings(self):
        """Load user settings from a JSON file."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                return settings
            except Exception as e:
                print(f"Error loading settings: {e}")
        return {"volume": 50, "theme_color": 128, "shuffle": False, "repeat": False}  # Default settings
