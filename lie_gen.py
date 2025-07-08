# Dictionary mit Attributen und deren Gegenteilen
attribute_opposites = {
    "largest": "smallest",
    "smallest": "largest",
    "highest": "lowest",
    "lowest": "highest",
    "longest": "shortest",
    "shortest": "longest",
    "oldest": "youngest",
    "youngest": "oldest",
    "strongest": "weakest",
    "weakest": "strongest",
    "fastest": "slowest",
    "slowest": "fastest",
    "richest": "poorest",
    "poorest": "richest",
    "most famous": "least famous",
    "least famous": "most famous",
    "densest": "thinnest",
    "thinnest": "densest",
    "most populated": "least populated",
    "least populated": "most populated",
    "tallest": "shortest",
    "deepest": "shallowest",
    "shallowest": "deepest",
    "widest": "narrowest",
    "narrowest": "widest",
    "heaviest": "lightest",
    "lightest": "heaviest",
    "most dangerous": "safest",
    "safest": "most dangerous",
    "hottest": "coldest",
    "coldest": "hottest",
    "most expensive": "cheapest",
    "cheapest": "most expensive",
    "stronger": "weaker",
    "weaker": "stronger",
    "newest": "oldest",
    "more powerful": "less powerful",
    "less powerful": "more powerful",
    "more developed": "less developed",
    "less developed": "more developed",
    "big": "small",
    "small": "big",
    "happy": "sad",
    "sad": "happy",
    "hot": "cold",
    "cold": "hot",
    "fast": "slow",
    "slow": "fast",
    "strong": "weak",
    "weak": "strong",
    "light": "dark",
    "dark": "light",
    "easy": "difficult",
    "difficult": "easy",
    "early": "late",
    "late": "early",
    "clean": "dirty",
    "dirty": "clean",
    "new": "old",
    "old": "new",
    "young": "old",
    "rich": "poor",
    "poor": "rich",
    "kind": "mean",
    "mean": "kind",
    "safe": "dangerous",
    "dangerous": "safe",
    "empty": "full",
    "full": "empty",
    "tall": "short",
    "short": "tall",
    "wide": "narrow",
    "narrow": "wide",
    "open": "closed",
    "closed": "open",
    "sharp": "dull",
    "dull": "sharp",
    "quiet": "loud",
    "loud": "quiet",
    "alive": "dead",
    "dead": "alive",
    "dry": "wet",
    "wet": "dry",
    "true": "false",
    "false": "true",
    "hard": "soft",
    "soft": "hard",
    "thick": "thin",
    "thin": "thick",
    "beautiful": "ugly",
    "ugly": "beautiful",
    "friendly": "hostile",
    "hostile": "friendly"
}



# Funktion zum leichten Verändern von Zahlen
def slightly_wrong_numbers(text):
    words = text.split()
    new_words = []
    for word in words:
        if word.isdigit():  # Wenn das Wort eine Zahl ist
            number = int(word)
            change = int(number * 0.25)
            number += change if number % 2 == 0 else -change  # Manchmal hoch, manchmal runter
            new_words.append(str(number))
        else:
            new_words.append(word)
    return " ".join(new_words)

# Funktion zum Umkehren von Attributen
def opposite_attribute(text):
    words = text.split()
    new_words = []
    for word in words:
        clean_word = word.lower().strip(",.!?")  # Wort kleinschreiben und bereinigen
        if clean_word in attribute_opposites:
            replacement = attribute_opposites[clean_word]
            if word[0].isupper():  # Wenn das Wort mit einem Großbuchstaben beginnt
                replacement = replacement.capitalize()
            new_words.append(replacement)
        else:
            new_words.append(word)
    return " ".join(new_words)

# Funktion, die die Bedeutung umkehrt (z.B. "is" -> "is not")
def flip_meaning(text):
    words = text.split()
    new_words = []
    for word in words:
        if word.lower() == "is":
            new_words.append("is not")
        elif word.lower() == "are":
            new_words.append("are not")
        elif word.lower() == "was":
            new_words.append("was not")
        elif word.lower() == "were":
            new_words.append("were not")
        elif word.lower() == "will":
            new_words.append("will not")
        else:
            new_words.append(word)
    return " ".join(new_words)


def generate_lie(true_fact):
    try:
        # Wenn die erste Funktion true_fact verändert, benutze sie
        modified_text = slightly_wrong_numbers(true_fact)
        if modified_text != true_fact:
            return modified_text
        else:
            # Wenn die erste Funktion nichts verändert hat, versuche die zweite
            modified_text = opposite_attribute(true_fact)
            if modified_text != true_fact:
                return modified_text
            else:
                # Wenn auch die zweite nichts verändert hat, versuche die dritte
                modified_text = flip_meaning(true_fact)
                return modified_text

    except Exception as e:
        print(f"An error has occurred: {e}")
