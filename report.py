import os
import sys
import subprocess

try:
    import pygame

    try:
        pygame.mixer.init()
    except Exception:
        # If mixer init fails, treat pygame as unavailable for playback
        pygame = None
except ImportError:
    pygame = None


def report():
    # Path to music file - replace with actual path to your music file
    music_file = "cat.mp3"

    # Check if pygame is available and music file exists
    if pygame is None:
        print("Pygame not available for music playback.")
        print("If you want pygame playback, install it with:")
        print("    python -m pip install pygame")

        # Fallback: try to open file with the OS default application
        if not os.path.exists(music_file):
            print(f"Music file {music_file} not found")
            return

        try:
            if sys.platform.startswith('win'):
                # Opens the file with the default associated application on Windows
                os.startfile(os.path.abspath(music_file))
                print(f"Opened {music_file} with the default application.")
                return
            elif sys.platform == 'darwin':
                subprocess.run(["open", music_file], check=False)
                print(f"Opened {music_file} with the default application.")
                return
            else:
                # Try xdg-open on many Linux systems
                subprocess.run(["xdg-open", music_file], check=False)
                print(f"Opened {music_file} with the default application.")
                return
        except Exception as e:
            print(f"Could not open {music_file} with OS default player: {e}")
            return

    if not os.path.exists(music_file):
        print(f"Music file {music_file} not found")
        return

    try:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        # Keep the program running while music plays
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    except Exception as e:
        print(f"Error playing music: {e}")


if __name__ == "__main__":
    report()
