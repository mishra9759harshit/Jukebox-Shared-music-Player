import logging
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from modules.audio import Audio
from modules.storage import Storage
from modules.sync import Sync
from modules.network import Network
from modules.utils import Utils

# Configure logging for detailed error logging
logging.basicConfig(filename="party_jukebox_errors.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.debug("Application started.")

class PartyJukeboxApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.storage = Storage()  # Initialize Storage class
            self.audio = Audio()  # Initialize Audio class
            self.network = Network()  # Initialize Network class
            self.sync = Sync(self.network)  # Initialize Sync class
            self.playlist = self.storage.load_playlist()  # Load playlist
            self.settings = self.storage.load_settings()  # Load settings
            self.preferences = Utils.load_preferences()  # Load preferences from JSON
            print("Initialization successful.")
        except Exception as e:
            logging.error(f"Error during initialization: {e}")
            print(f"Error during initialization: {e}")

    def build(self):
        """Build the app interface."""
        try:
            self.theme_cls.primary_palette = "BlueGray"  # Set the default theme
            print("Building the UI...")
            return Builder.load_file("kivy_ui/main.kv")  # Load the main UI
        except Exception as e:
            logging.error(f"Error while building UI: {e}")
            print(f"Error while building UI: {e}")
            return None

    def change_screen(self, screen_name):
        """Animate screen transitions."""
        sm = self.root.ids.screen_manager
        sm.transition = SlideTransition(direction="left")
        sm.current = screen_name

    def play_song(self, song_path):
        """Play the selected song using the Audio class and sync across devices."""
        try:
            print("Attempting to play song...")  # Debugging statement
            self.audio.play(song_path)
            self.sync.sync_music(song_path, self.audio.song_length)  # Sync the song across devices
        except Exception as e:
            logging.error(f"Error playing song {song_path}: {e}")
            print(f"Error playing song: {e}")

    def pause_song(self):
        """Pause the currently playing song."""
        try:
            self.audio.pause()
        except Exception as e:
            logging.error(f"Error pausing song: {e}")
            print(f"Error pausing song: {e}")

    def unpause_song(self):
        """Unpause the song."""
        try:
            self.audio.unpause()
        except Exception as e:
            logging.error(f"Error unpausing song: {e}")
            print(f"Error unpausing song: {e}")

    def stop_song(self):
        """Stop the currently playing song."""
        try:
            self.audio.stop()
        except Exception as e:
            logging.error(f"Error stopping song: {e}")
            print(f"Error stopping song: {e}")

    def add_song_to_playlist(self, song_path):
        """Add a song to the playlist and save it."""
        try:
            if song_path not in self.playlist:
                self.playlist.append(song_path)
                self.storage.save_playlist(self.playlist)  # Save the updated playlist
                self.update_playlist_ui()
        except Exception as e:
            logging.error(f"Error adding song to playlist: {e}")
            print(f"Error adding song to playlist: {e}")

    def remove_song_from_playlist(self, song_path):
        """Remove a song from the playlist and save it."""
        try:
            if song_path in self.playlist:
                self.playlist.remove(song_path)
                self.storage.save_playlist(self.playlist)  # Save the updated playlist
                self.update_playlist_ui()
        except Exception as e:
            logging.error(f"Error removing song from playlist: {e}")
            print(f"Error removing song from playlist: {e}")

    def update_playlist_ui(self):
        """Update the playlist UI to reflect changes."""
        # This function can be used to update the playlist UI (e.g., refresh the list view)
        pass

    def save_user_preferences(self):
        """Save user preferences (volume, theme, etc.) using the Utils class."""
        try:
            preferences = {
                "volume": self.settings["volume"],
                "theme_color": self.settings["theme_color"],
                "shuffle": self.settings["shuffle"],
                "repeat": self.settings["repeat"]
            }
            Utils.save_preferences(preferences)  # Save preferences to a JSON file
        except Exception as e:
            logging.error(f"Error saving preferences: {e}")
            print(f"Error saving preferences: {e}")

    def load_user_preferences(self):
        """Load user preferences from the JSON file."""
        try:
            self.preferences = Utils.load_preferences()
            self.settings.update(self.preferences)  # Update settings with saved preferences
            self.audio.set_volume(self.settings["volume"])
            self.theme_cls.primary_color = self.settings["theme_color"]
        except Exception as e:
            logging.error(f"Error loading preferences: {e}")
            print(f"Error loading preferences: {e}")

    def show_qr_code(self, party_code):
        """Generate and show a QR code for joining the party."""
        try:
            qr_texture = Utils.generate_qr_code(party_code)  # Get the QR code texture
            if qr_texture:
                self.root.ids.qr_code.texture = qr_texture  # Display the QR code on the UI
        except Exception as e:
            logging.error(f"Error generating QR code: {e}")
            print(f"Error generating QR code: {e}")

    def start_party(self):
        """Start a party as the host."""
        try:
            self.network.start_server()
            print("Party started. Waiting for guests...")
        except Exception as e:
            logging.error(f"Error starting party: {e}")
            print(f"Error starting party: {e}")

    def join_party(self, ip):
        """Join an existing party as a client."""
        try:
            self.network.connect_to_server(ip)
            print(f"Connected to party at {ip}.")
        except Exception as e:
            logging.error(f"Error joining party at {ip}: {e}")
            print(f"Error joining party: {e}")

    def send_message(self, message):
        """Send sync control messages (e.g., play, pause, sync)."""
        try:
            self.network.send_message(message)
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            print(f"Error sending message: {e}")

    def change_theme(self, value):
        """Update the app's theme color and save the preference."""
        try:
            self.settings["theme_color"] = value
            self.theme_cls.primary_color = value
            self.save_user_preferences()  # Save updated theme color preference
        except Exception as e:
            logging.error(f"Error changing theme: {e}")
            print(f"Error changing theme: {e}")

    def update_volume(self, value):
        """Update the volume setting and save the preference."""
        try:
            self.settings["volume"] = value
            self.audio.set_volume(value)
            self.save_user_preferences()  # Save updated volume preference
        except Exception as e:
            logging.error(f"Error updating volume: {e}")
            print(f"Error updating volume: {e}")

    def toggle_shuffle(self, active):
        """Enable or disable shuffle mode."""
        try:
            self.settings["shuffle"] = active
            self.save_user_preferences()
        except Exception as e:
            logging.error(f"Error toggling shuffle: {e}")
            print(f"Error toggling shuffle: {e}")

    def toggle_repeat(self, active):
        """Enable or disable repeat mode."""
        try:
            self.settings["repeat"] = active
            self.save_user_preferences()
        except Exception as e:
            logging.error(f"Error toggling repeat: {e}")
            print(f"Error toggling repeat: {e}")
