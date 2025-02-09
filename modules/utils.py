import qrcode
from kivy.core.image import Image as CoreImage
from io import BytesIO
import logging
import os

# Set up logging for error handling
log_file = "app_log.txt"
logging.basicConfig(filename=log_file, level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class Utils:
    @staticmethod
    def generate_qr_code(data):
        """
        Generate a QR code for sharing party details.
        
        :param data: The string data (e.g., party code, IP address) to be embedded in the QR code.
        :return: CoreImage object containing the QR code image.
        """
        try:
            qr = qrcode.make(data)  # Create QR code from data
            buffer = BytesIO()  # Create a buffer to store the image
            qr.save(buffer, format="PNG")  # Save image to buffer in PNG format
            buffer.seek(0)  # Rewind the buffer
            return CoreImage(buffer, ext="png").texture  # Return as texture
        except Exception as e:
            Utils.log_error(f"Error generating QR code: {e}")
            return None

    @staticmethod
    def log_error(message):
        """
        Log errors to a log file.
        
        :param message: The error message to log.
        """
        logging.error(message)
        print(f"Error logged: {message}")

    @staticmethod
    def format_duration(seconds):
        """
        Format a duration (in seconds) into a readable time format (mm:ss).
        
        :param seconds: The duration in seconds.
        :return: A formatted string in "mm:ss" format.
        """
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    @staticmethod
    def save_preferences(preferences, filename="preferences.json"):
        """
        Save user preferences (such as theme, volume, etc.) to a JSON file.
        
        :param preferences: Dictionary of user preferences.
        :param filename: The file to save the preferences (default is preferences.json).
        """
        import json
        try:
            with open(filename, "w") as file:
                json.dump(preferences, file, indent=4)
            print(f"Preferences saved to {filename}.")
        except Exception as e:
            Utils.log_error(f"Error saving preferences: {e}")

    @staticmethod
    def load_preferences(filename="preferences.json"):
        """
        Load user preferences from a JSON file.
        
        :param filename: The file to load the preferences (default is preferences.json).
        :return: The loaded preferences dictionary.
        """
        import json
        if os.path.exists(filename):
            try:
                with open(filename, "r") as file:
                    preferences = json.load(file)
                return preferences
            except Exception as e:
                Utils.log_error(f"Error loading preferences: {e}")
        else:
            return {}  # Return an empty dictionary if no preferences are found

