import menu
import leaderboard_utils


# Farben definieren
GREEN = "\033[92m"
RESET = "\033[0m"


MENU_ACTIONS = {
    1: menu.play_game,
    2: leaderboard_utils.show_leaderboard,
    3: leaderboard_utils.reset_leaderboard,
    4: menu.quit_game
}


def main():

    while True:
        menu.clear_screen()
        #menu.play_music()
        menu.print_main_menu()

        try:
            choice = menu.evaluate_menu_input(input(f"  {GREEN}Enter choice (1-4): {RESET}"))
        except ValueError as e:
            print(e)
            continue

        action = MENU_ACTIONS.get(choice)
        if action:
            action()
        else:
            print(f"    {GREEN}Invalid choice.{RESET}")


if __name__ == "__main__":
    main()