import time
import menu

def play_game():
    total_time = 3  # 3 Minuten in Sekunden
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed >= total_time:
            menu.display_game_over_screen(90)




if __name__ == '__main__':
    play_game()