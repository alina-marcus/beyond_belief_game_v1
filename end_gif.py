import pygame
from PIL import Image
import os


# === GIF laden von Datei ===
def gif_aus_datei_laden(pfad):
    return Image.open(pfad)

# === GIF in Pygame-kompatible Frames umwandeln und skalieren ===
def gif_zu_pygame_frames(gif, zielgroesse):
    frames = []
    try:
        while True:
            frame = gif.copy().convert("RGBA")
            pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
            # Frame auf Zielgröße skalieren
            pygame_frame = pygame.transform.scale(pygame_frame, zielgroesse)
            frames.append(pygame_frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

# === Soundsystem-Test ===
def sound_test():
    # print("Sound-Test wird durchgeführt...")

    # Prüfen, ob die Sound-Datei existiert
    sound_file = "data/pusten.wav"
    if not os.path.exists(sound_file):
        print(f"FEHLER: Sound-Datei '{sound_file}' nicht gefunden!")
        print(f"Aktuelles Verzeichnis: {os.getcwd()}")
        print("Verfügbare Dateien:")
        for file in os.listdir("."):
            print(f"  - {file}")
        return False

    # print(f"Sound-Datei '{sound_file}' gefunden!")
    return True

# === Hauptprogramm ===
def show_gif():
    pygame.init()

    # Verschiedene Mixer-Initialisierungsoptionen testen
    mixer_initialized = False
    mixer_options = [
        {"frequency": 44100, "size": -16, "channels": 2, "buffer": 4096},
        {"frequency": 48000, "size": -16, "channels": 2, "buffer": 2048},
        {"frequency": 22050, "size": -16, "channels": 1, "buffer": 512},
        {}  # Standardwerte
    ]

    for option in mixer_options:
        try:
            if option:
                pygame.mixer.quit()
                pygame.mixer.init(**option)
                # print(f"Mixer initialisiert mit: {option}")
            else:
                pygame.mixer.quit()
                pygame.mixer.init()
                # print("Mixer mit Standardwerten initialisiert")
            mixer_initialized = True
            break
        except Exception as e:
            print(f"Mixer-Initialisierung fehlgeschlagen: {e}")

    if not mixer_initialized:
        print("WARNUNG: Konnte Mixer nicht initialisieren. Keine Soundausgabe möglich.")

    # Sound-Datei testen
    sound_exists = sound_test()
    sound_method = None

    # Bildschirmgröße ermitteln
    info = pygame.display.Info()
    bildschirm_breite = info.current_w
    bildschirm_hoehe = info.current_h
    bildschirm_groesse = (bildschirm_breite, bildschirm_hoehe)

    # GIF laden und auf Bildschirmgröße skalieren
    try:
        gif = gif_aus_datei_laden("data/BIGGY.gif")
        frames = gif_zu_pygame_frames(gif, bildschirm_groesse)
    except Exception as e:
        print(f"Fehler beim Laden des GIFs: {e}")
        pygame.quit()
        return

    # Vollbild-Modus aktivieren
    screen = pygame.display.set_mode(bildschirm_groesse, pygame.FULLSCREEN)
    pygame.display.set_caption("GIF mit Pustesound")
    clock = pygame.time.Clock()

    # Versuche Sound mit verschiedenen Methoden zu laden
    if mixer_initialized and sound_exists:
        # print("Versuche Sound zu laden...")
        try:
            # Methode 1: pygame.mixer.Sound
            pust_sound = pygame.mixer.Sound("data/pusten.wav")
            pust_sound.set_volume(1.0)
            sound_channel = pygame.mixer.Channel(0)
            sound_channel.play(pust_sound, loops=-1)
            # print("Sound mit pygame.mixer.Sound geladen und abgespielt")
            sound_method = "sound"
        except Exception as e1:
            print(f"Fehler mit pygame.mixer.Sound: {e1}")
            try:
                # Methode 2: pygame.mixer.music
                pygame.mixer.music.load("data/pusten.wav")
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(-1)
                # print("Sound mit pygame.mixer.music geladen und abgespielt")
                sound_method = "music"
            except Exception as e2:
                print(f"Fehler mit pygame.mixer.music: {e2}")
                sound_method = None

    # Animation starten
    running = True
    frame_index = 0
    frame_delay = 100  # Millisekunden zwischen Frames
    last_update = pygame.time.get_ticks()

    # print("Animation startet...")
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

    # Aufräumen beim Beenden
    if sound_method == "sound":
        sound_channel.stop()
    elif sound_method == "music":
        pygame.mixer.music.stop()

    pygame.quit()
    # print("Programm beendet.")