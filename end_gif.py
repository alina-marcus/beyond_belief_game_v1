import os
import pygame
from PIL import Image


def load_gif_from_file(path):
    """
    Loads a GIF image from a file.

    Args:
        path (str): File path to the GIF.

    Returns:
        PIL.Image.Image: The opened GIF image.
    """
    return Image.open(path)


def gif_to_pygame_frames(gif, target_size):
    """
    Converts a GIF into a list of Pygame-compatible frames.

    Args:
        gif (PIL.Image.Image): GIF image object.
        target_size (tuple): Target size as (width, height).

    Returns:
        list: List of scaled Pygame surfaces (frames).
    """
    frames = []
    try:
        while True:
            frame = gif.copy().convert("RGBA")
            pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
            pygame_frame = pygame.transform.scale(pygame_frame, target_size)
            frames.append(pygame_frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames


def sound_test():
    """
    Checks if the sound file exists.

    Returns:
        bool: True if the file exists, otherwise False.
    """
    sound_file = "data/pusten.wav"
    if not os.path.exists(sound_file):
        print(f"ERROR: Sound file '{sound_file}' not found!")
        print(f"Current directory: {os.getcwd()}")
        print("Available files:")
        for file in os.listdir("."):
            print(f"  - {file}")
        return False

    return True


def show_gif():
    """
    Displays a GIF in fullscreen mode and optionally plays a looping sound.
    """
    pygame.init()

    # Try initializing mixer with various settings
    mixer_initialized = False
    mixer_options = [
        {"frequency": 44100, "size": -16, "channels": 2, "buffer": 4096},
        {"frequency": 48000, "size": -16, "channels": 2, "buffer": 2048},
        {"frequency": 22050, "size": -16, "channels": 1, "buffer": 512},
        {}
    ]

    for option in mixer_options:
        try:
            pygame.mixer.quit()
            pygame.mixer.init(**option) if option else pygame.mixer.init()
            mixer_initialized = True
            break
        except Exception as e:
            print(f"Mixer initialization failed: {e}")

    if not mixer_initialized:
        print("WARNING: Could not initialize mixer. No sound output possible.")

    # Check if sound file exists
    sound_exists = sound_test()
    sound_method = None

    # Get display size
    info = pygame.display.Info()
    screen_size = (info.current_w, info.current_h)

    # Load and prepare GIF
    try:
        gif = load_gif_from_file("data/BIGGY.gif")
        frames = gif_to_pygame_frames(gif, screen_size)
    except Exception as e:
        print(f"Error loading GIF: {e}")
        pygame.quit()
        return

    # Setup fullscreen window
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    pygame.display.set_caption("GIF with blowing sound")
    clock = pygame.time.Clock()

    # Play sound if possible
    if mixer_initialized and sound_exists:
        try:
            puff_sound = pygame.mixer.Sound("data/pusten.wav")
            puff_sound.set_volume(1.0)
            sound_channel = pygame.mixer.Channel(0)
            sound_channel.play(puff_sound, loops=-1)
            sound_method = "sound"
        except Exception as e1:
            print(f"Error with pygame.mixer.Sound: {e1}")
            try:
                pygame.mixer.music.load("data/pusten.wav")
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(-1)
                sound_method = "music"
            except Exception as e2:
                print(f"Error with pygame.mixer.music: {e2}")
                sound_method = None

    # Animate GIF frames
    running = True
    frame_index = 0
    frame_delay = 100  # milliseconds between frames
    last_update = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        now = pygame.time.get_ticks()
        if now - last_update > frame_delay:
            frame_index = (frame_index + 1) % len(frames)
            last_update = now

        screen.blit(frames[frame_index], (0, 0))
        pygame.display.flip()
        clock.tick(60)

    # Stop sound on exit
    if sound_method == "sound":
        sound_channel.stop()
    elif sound_method == "music":
        pygame.mixer.music.stop()

    pygame.quit()


if __name__ == "__main__":
    show_gif()
