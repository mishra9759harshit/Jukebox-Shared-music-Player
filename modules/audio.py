import pygame

class Audio:
    def __init__(self):
        """Initialize pygame mixer for audio playback."""
        pygame.mixer.init()
        self.current_song = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.5  # Default volume set to 50%
        pygame.mixer.music.set_volume(self.volume)

    def play(self, song_path):
        """Play the selected song."""
        if song_path != self.current_song:
            pygame.mixer.music.load(song_path)  # Load new song
            pygame.mixer.music.play()  # Play the song
            self.current_song = song_path  # Set current song
            self.is_playing = True
            self.is_paused = False
        else:
            self.unpause()  # If the same song is selected, unpause it if paused.

    def pause(self):
        """Pause the current song."""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
            print(f"Paused: {self.current_song}")

    def unpause(self):
        """Unpause the current song."""
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.is_paused = False
            print(f"Resumed: {self.current_song}")

    def stop(self):
        """Stop the current song."""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_song = None
        print("Stopped music playback.")

    def set_volume(self, volume):
        """Set the volume of the music (0.0 to 1.0)."""
        self.volume = volume / 100  # Convert volume to 0-1 range
        pygame.mixer.music.set_volume(self.volume)
        print(f"Volume set to {volume}%.")

    def shuffle(self):
        """Shuffle the playlist (Future functionality)."""
        print("Shuffle functionality not implemented yet.")
        # For future, add shuffle logic here, like randomizing the playlist.

    def repeat(self):
        """Repeat the current song (Future functionality)."""
        print("Repeat functionality not implemented yet.")
        # Future logic to repeat the current song will go here.
