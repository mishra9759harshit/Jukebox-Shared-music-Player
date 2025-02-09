import time
import threading
import json

class Sync:
    def __init__(self, network):
        self.network = network  # Instance of the Network class for communication
        self.is_playing = False
        self.current_song = None
        self.start_time = None
        self.song_length = 0  # The length of the current song in seconds

    def sync_music(self, song, song_length):
        """Sync the music across all devices."""
        self.current_song = song
        self.song_length = song_length  # Set the song length for sync calculation
        self.start_time = time.time()  # Mark the time the song starts playing
        self.is_playing = True
        self.network.broadcast(f"PLAY {song}")  # Broadcast the play message
        print(f"Syncing song {song} across all devices...")

        # Start a background thread to handle real-time synchronization
        threading.Thread(target=self.start_sync, daemon=True).start()

    def start_sync(self):
        """Send sync messages to clients to keep the music in sync."""
        while self.is_playing:
            elapsed_time = time.time() - self.start_time
            self.network.broadcast(f"SYNC {self.current_song} {elapsed_time}")
            time.sleep(1)  # Broadcast every second to keep everything in sync

    def sync_handler(self, data):
        """Handle sync messages from other devices."""
        if data.startswith("SYNC"):
            _, song, elapsed_time = data.split(" ")
            print(f"Syncing song {song} to {elapsed_time} seconds")
            self.sync_playback(song, float(elapsed_time))

        elif data.startswith("PLAY"):
            _, song = data.split(" ")
            print(f"Starting the song {song}")
            self.sync_music(song, self.song_length)

        elif data.startswith("PAUSE"):
            print("Pausing playback on all devices.")
            self.pause_playback()

    def sync_playback(self, song, elapsed_time):
        """Ensure playback is in sync with the host by adjusting the playback time."""
        if self.current_song == song:
            # Adjust playback time to sync with the host (dummy function to simulate time adjustment)
            print(f"Syncing song {song} to {elapsed_time} seconds")
            # Implement actual audio seek logic here if needed

    def pause_playback(self):
        """Pause music on all devices."""
        print(f"Pausing playback of song {self.current_song}")
        self.is_playing = False
        self.network.broadcast(f"PAUSE {self.current_song}")
