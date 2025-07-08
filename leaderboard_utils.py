import os
import json

GREEN = "\033[92m"
RESET = "\033[0m"

LEADERBOARD_FILE = "data/leaderboard.json"

def load_leaderboard():
    """Loads the leaderboard from a JSON file."""
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return {}

def save_leaderboard(leaderboard):
    """Saves the leaderboard to a JSON file."""
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4, sort_keys=True)

def update_leaderboard_if_high_score(player_name, score):
    """Updates the leaderboard if the score is in the top 5.
    Returns True if it's a high score, False otherwise.
    """

    # Score von 0 wird ignoriert
    if score == 0:
        return False
    
    leaderboard = load_leaderboard()
    all_scores = list(leaderboard.items()) + [(player_name, score)]
    all_scores.sort(key=lambda x: (-x[1], x[0]))
    new_top_five = dict(all_scores[:5])

    is_highscore = (player_name, score) in all_scores[:5]
    if is_highscore:
        save_leaderboard(new_top_five)

    return is_highscore

def reset_leaderboard():
    """Clears the leaderboard."""
    print(f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    confirm = input("Are you sure you want to reset the leaderboard? (y/n): ")
    print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

    if confirm.lower() == "y":
        save_leaderboard({})
        print(f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
        print(" Leaderboard has been reset.{RESET}")
        print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
        print(f"{RESET}")



def show_leaderboard():
    """Lists all players and their scores."""
    leaderboard = load_leaderboard()
    leaderboard_list = list(leaderboard.items())
    print(
        f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print()
    print("      █     ▄███▄   ██▄  ██▄   ▄███▄   █▄▄▄▄     ███   ████▄ ██   █▄▄▄▄ ██▄")
    print("      █     █▀   ▀  █ █  █  █  █▀   ▀  █  ▄▀     █  █  █   █ █ █  █  ▄▀ █  █")
    print("      █     ██▄▄    █▄▄█ █   █ ██▄▄    █▀▀▌      █ ▀ ▄ █   █ █▄▄█ █▀▀▌  █   █")
    print("      ███▄  █▄   ▄▀ █  █ █  █  █▄   ▄▀ █  █      █  ▄▀ ▀████ █  █ █  █  █  █")
    print("          ▀ ▀███▀      █ ███▀  ▀███▀     █       ███            █   █   ███▀")
    print("                      █                 ▀                      █   ▀")
    print("                     ▀                                        ▀    ")
    print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print(
        f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    # SORT THE LEADERBOARD LIST
    sorted_scores = sorted(leaderboard_list, key=lambda x: x[1], reverse=True)
    print(f"    RANK\t\tPLAYER\t\t\t\t\t\tSCORE")
    for index, (player, score) in enumerate(sorted_scores, start=1):
        print(f"    {index:<4}\t\t{player.upper():<20}\t\t{score:>5}")
    print(
        f"╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    input(f"{GREEN}Press Enter to return to main menu. {RESET}")


if __name__ == "__main__":
    show_leaderboard()
