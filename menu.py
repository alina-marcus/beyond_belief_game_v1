import sys
import os
import pygame

import end_gif
import game_logic
import leaderboard_utils

# Terminal color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def play_music():
    """Plays background music if the file exists."""
    pygame.mixer.init()
    music_path = "/Users/alinamarcus/Library/Mobile Documents/com~apple~CloudDocs/beyond_belief_game/music/xxx.wav"
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    else:
        print(f"{GREEN}Music file not found at: {music_path}{RESET}")

def clear_screen():
    """Clears the terminal screen."""
    if os.name == 'nt':
        os.system('cls')
    elif 'TERM' in os.environ:
        os.system('clear')
    else:
        print("\n" * 100)

def get_player_name():
    """Prompts the player to enter their name."""
    print(f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    player_name = input(f"  {GREEN}State your name as you step into the unknown: {RESET}").strip()
    print(f"{GREEN}╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print(
        f"  {GREEN}🕵️ Hello {player_name}, welcome to the game of truth and lies.\n"
        f"     Two truths, one lie... but only one chance to find it.{RESET}\n"
        f"{GREEN}╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣")
    input("  Press Enter to continue.")
    return player_name

def play_game():
    """Starts a new game round."""
    player_name = get_player_name()
    total_points = game_logic.play_game()

    if leaderboard_utils.update_leaderboard_if_high_score(player_name, total_points):
        print(f"    {GREEN}NEW HIGHSCORE!{RESET}")
        leaderboard_utils.show_leaderboard()

    clear_screen()
    display_game_over_screen(total_points)
    input("    Press Enter to return to the main menu. ")

def quit_game():
    """Exits the game with farewell message and animation."""
    print(f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{GREEN}❌     The game has been quit. The truth remains, waiting until we meet again.                                  ❌{RESET}")
    print(f"{GREEN}╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    end_gif.show_gif()
    sys.exit()

def print_main_menu():
    """Displays the main menu."""
    print(f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║ ▄▄▄▄     ▓█████▓  ██   ██▓  ▒█████▀    ███▄   ██   ▓█████▄    ▄▄▄▄   ▓█████   ██▓      ██▓  ▓██████  ████████ ║")
    print("║ ▓█████▄   ▓█      ▒██  ██▒  ▒█▒   ██▒  ██ ▀█  ██   ▒██▀ ██▌  ▓█████▄ ▓█   ▀  ▓██▒      ▓██  ▒▓█      ▓██      ║")
    print("║ ▒██▒ ▄█  █▒███     ▒██ ██░  ▒█░   ██▒  ██  ▀█ █▒   ██    █▌  ▒██▒ ▄█ █▒███   ▒██░      ▒██  ▒▒████   ▒██████  ║")
    print("║ ▒██░█▀    ▒▓█  ▄  ░ ▐██▓▒   ██   ██░▓  █▒   ▐▌█▒   ▓█▄   █▌  ▒██░█▀  ▒▓█  ▄  ▒██░      ░██  ░▒▓█  ▄  ░██▒  ░  ║")
    print("║ ░▓█  ▀█  ▓░▒████▒ ░ ██▒░    ████▓▒░▒█  █░    ██  ░ ▒████▓    ░▓█  ▀█ ▓░▒████▒ ░██████▒ ░██░ ░▒█████  ▒██░     ║")
    print("╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣")
    print("║ Welcome to Beyond Belief: Fact or Fiction – The game where knowledge meets instinct                          ║")
    print("║ Three statements. One is a lie. Will your instincts guide you?                                               ║")
    print("║ Behind every fact lies a shadow. Find the one that doesn't belong.                                           ║")
    print("╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣")
    print("║ Menu:                                                                                                        ║")
    print("║   1. Play Game                                                                                               ║")
    print("║   2. Show Leaderboard                                                                                        ║")
    print("║   3. Reset Leaderboard                                                                                       ║")
    print("║   4. Quit Game                                                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

def evaluate_menu_input(user_input):
    """Validates and converts the user's menu selection."""
    valid_choices = {'1', '2', '3', '4'}
    user_input = user_input.strip()

    if user_input in valid_choices:
        return int(user_input)
    else:
        raise ValueError(f"{GREEN}  Invalid menu option. Please enter a number between 1 and 4.{RESET}")

def display_game_over_screen(points_count):
    """Displays the game over screen with ASCII art and score."""
    ascii_art = f"""{RED}
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║  ▄█████    ▄▄▄        ███▄ ▄███▓ ▓█████     ▒█████   ██▒   █▓▓ █████  ███▀██▄                                 ║
║  ██▒  █▒  ▒████▄     ▓██▒▀█▀ ██▒ ▓█   ▀    ▒██▒  ██▒ ▓██░   █▒ ▓█   ▀ ▓██  ▒██▒                               ║
║  ███░▄▄▄  ▒██  ▀█▄   ▓██    ▓██░ ▒███      ▒██░  ██▒ ▓██  █▒░ ▒███    ▓██ ░▄█▒                                ║
║  ███  ██▓ ░██▄▄▄▄██  ▒██    ▒██  ▒▓█  ▄    ▒██   ██░  ▒██ █░ ░▒▓█  ▄  ▒██▀▀█▄                                 ║
║  ░▒████▀▒  ▓█   ▓██ ▒▒██▒   ░██▒ ░▒████▒   ░ ████▓▒░   ▒██░  ░▒████▒░ ██▓  ▒█▒                                ║
║   ░▒    ▒  ▒▒   ▓▒█ ░░ ▒░   ░  ░░ ░ ▒░ ░   ░ ▒░▒░▒░    ░▐░   ░░ ▒░ ░░  ▒▓ ░▒▓░                                ║
║    ░    ░   ▒   ▒▒  ░░  ░      ░ ░  ░  ░     ░ ▒ ▒░    ░ ░░   ░ ░  ░   ░▒ ░ ▒░                                ║
║  ░ ░    ░   ░   ▒    ░      ░       ░      ░ ░ ░ ▒       ░░     ░      ░░   ░                                 ║
║      ░       ░   ░       ░       ░  ░       ░ ░        ░     ░  ░   ░                                         ║
║                                                        ░                                                      ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝                                                         
{RESET}"""
    print(ascii_art)
    print(f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print(f"  Your final score: {points_count}")
    print(f"╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
