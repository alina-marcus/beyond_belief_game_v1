import random
import os
import textwrap
import menu
import time

import gpt_api
import wiki_api
import lie_gen

GREEN = "\033[92m"
RED = '\033[91m'
RESET = "\033[0m"

LIVES = 3
TOTAL_TIME = 60 * 5 # 5 mi

truth_quotes = [
    "You're right — this story was entirely made up.",
    "Correct — none of this was actually true.",
    "As believable as it sounded, it was pure fiction.",
    "This was completely fabricated.",
    "Sometimes lies sound more realistic than the truth — and this was one of them.",
    "Nope, it didn’t happen like that — or at all.",
    "This account was invented, not reported.",
    "Scientists never heard of this — because it’s fake.",
    "There are no police records — we made it up.",
    "We did make it up — and you caught it.",
    "There were no eyewitnesses — just imagination.",
    "It sounds like a fairytale because it is one.",
    "The origins of this story? Our imagination.",
    "As convincing as it is — it’s not real.",
    "A story that bends reality — all the way into fiction."
]

lie_quotes = [
    "You were wrong. This actually happened.",
    "Sorry, you made a mistake — this story is true.",
    "It wasn’t a trick — it really happened.",
    "You were mistaken — this story is real.",
    "Actually, this is really what happened.",
    "It may sound unbelievable, but it’s true.",
    "This wasn’t made up — it really happened.",
    "You underestimated us — this story is real.",
    "It wasn’t a joke — it actually happened.",
    "You were wrong — these events really occurred.",
    "The truth is, it happened exactly like this.",
    "It wasn’t an invention — this story is truly real.",
    "You thought we fooled you, but this story is actually true.",
    "There’s no doubt — this really happened.",
    "We tested you — and you were wrong."
]

def clear_screen():
    """Clears the screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        if 'TERM' in os.environ:
            os.system('clear')
        else:
            print("\n" * 100)

def get_sentences_for_game():
    page_title, sentences = wiki_api.get_valid_wikipedia_page_info(spooky=True)
    selected_sentences = random.sample(sentences[:6], 3)
    lie_index = random.randrange(3)
    original_sentence = selected_sentences[lie_index]

    attempts = 0
    while ('=' in original_sentence or
           any(char.isdigit() for char in original_sentence) or
           attempts > 5):
        selected_sentences = random.sample(sentences[:6], 3)
        original_sentence = selected_sentences[lie_index]
        attempts += 1

    #selected_sentences[lie_index] = lie_gen.generate_lie(original_sentence)
    selected_sentences[lie_index] = gpt_api.get_gpt_lie(original_sentence)

    return page_title, selected_sentences, lie_index

def print_boxed_text(lines, title=None):
    """Prints a formatted box with optional title"""
    max_width = 117  # angepasste Breite
    print(f"{GREEN}╔" + "═" * max_width + "╗")
    if title:
        title_lines = textwrap.wrap(title, max_width)
        for line in title_lines:
            print(f" {line.ljust(max_width)} ")
    for line in lines:
        wrapped = textwrap.wrap(line, max_width)
        for w_line in wrapped:
            print(f" {w_line.ljust(max_width)} ")
    print("╚" + "═" * max_width + "╝" + f"{RESET}")

def print_lives_and_points(lives, points, time_left_formatted):
    lives_str = f"Lives: {lives * '❤️ '}".strip()
    points_str = f"Points: {points}"
    time_left_str = f"    Time Left: {time_left_formatted}"

    max_width = 117
    left_section_width = len(lives_str) + 1
    right_section_width = len(points_str) + 1
    time_section_width = len(time_left_str)

    total_content_width = left_section_width + right_section_width + time_section_width
    middle_spacing = (max_width - total_content_width) // 2

    line = f"{lives_str}{' ' * middle_spacing}{time_left_str}{' ' * middle_spacing}{points_str}"

    print(f"{GREEN}╔" + "═" * max_width + "╗")
    print(f" {line.ljust(max_width)} ")
    print(f"╚" + "═" * max_width + "╝" + f"{RESET}")


def print_wrapped_sentence(index, sentence):
    max_width = 117
    wrapped = textwrap.wrap(sentence, width=max_width - 5)  # Platz für Nummerierung
    print("╔" + "═" * max_width + "╗")
    for i, line in enumerate(wrapped):
        if i == 0:
            print(f" {index}.  {line.ljust(max_width - 5)} ")
        else:
            print(f"      {line.ljust(max_width - 5)} ")
    print("╚" + "═" * max_width + "╝")


def display_sentences(page_title, sentences):
    print_boxed_text([], title=f"    Wikipedia Article: {page_title}")
    for idx, sentence in enumerate(sentences, 1):
        print_wrapped_sentence(idx, sentence)

def main_game_loop():
    page_title, sentences, lie_index = get_sentences_for_game()
    display_sentences(page_title, sentences)
    print_boxed_text(["    What's the lie? (1-3)", ""])
    while True:
        try:
            choice = int(input(f"{GREEN}     Type here and press Enter: {RESET}"))
            if choice not in [1, 2, 3]:
                print(f"{RED}     Please enter a number between 1 and 3.{RESET}")
                continue
        except ValueError:
            print(f"{RED}     Invalid input. Please enter a number (1, 2, or 3).{RESET}")
            continue
        break

    if choice == lie_index + 1:
        answer = random.choice(truth_quotes)
        print(f"     ✅ {GREEN}{answer} ✅{RESET}")
        return True
    else:
        answer = random.choice(lie_quotes)
        print(f"     ❌ {RED}{answer} ❌")
        print(f"     The correct answer was: {lie_index + 1}{RESET}")
        return False

def play_game():
    lives_count = LIVES
    points_count = 0

    total_time = TOTAL_TIME
    start_time = time.time()
    while True:
        clear_screen()
        elapsed = time.time() - start_time
        time_left = total_time - elapsed
        minutes_left = int(time_left // 60)
        seconds_left = int(time_left % 60)
        time_left_formatted = f"{minutes_left:02}:{seconds_left:02}"
        print_lives_and_points(lives_count, points_count, time_left_formatted)
        if main_game_loop():
            points_count += 1
            print_boxed_text([f"    You have {points_count} point!" if points_count == 1 else f"You have {points_count} points!"])
        else:
            lives_count -= 1
            if lives_count > 0:
                print_boxed_text([f"    You have {lives_count} {'life' if lives_count == 1 else 'lives'} left!"])
            if lives_count == 0:
                menu.display_game_over_screen(points_count)
                break

        elapsed = time.time() - start_time
        if elapsed >= total_time:
            menu.display_game_over_screen(points_count)
            break

        input(f"{GREEN}     Press Enter to continue {RESET}")
    return points_count

if __name__ == "__main__":
    play_game()

