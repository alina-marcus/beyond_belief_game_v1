# Dictionary mapping attributes to their opposites
attribute_opposites = {
    "largest": "smallest", "smallest": "largest",
    "highest": "lowest", "lowest": "highest",
    "longest": "shortest", "shortest": "longest",
    "oldest": "youngest", "youngest": "oldest",
    "strongest": "weakest", "weakest": "strongest",
    "fastest": "slowest", "slowest": "fastest",
    "richest": "poorest", "poorest": "richest",
    "most famous": "least famous", "least famous": "most famous",
    "densest": "thinnest", "thinnest": "densest",
    "most populated": "least populated", "least populated": "most populated",
    "tallest": "shortest", "deepest": "shallowest", "shallowest": "deepest",
    "widest": "narrowest", "narrowest": "widest",
    "heaviest": "lightest", "lightest": "heaviest",
    "most dangerous": "safest", "safest": "most dangerous",
    "hottest": "coldest", "coldest": "hottest",
    "most expensive": "cheapest", "cheapest": "most expensive",
    "stronger": "weaker", "weaker": "stronger",
    "newest": "oldest",
    "more powerful": "less powerful", "less powerful": "more powerful",
    "more developed": "less developed", "less developed": "more developed",
    "big": "small", "small": "big",
    "happy": "sad", "sad": "happy",
    "hot": "cold", "cold": "hot",
    "fast": "slow", "slow": "fast",
    "strong": "weak", "weak": "strong",
    "light": "dark", "dark": "light",
    "easy": "difficult", "difficult": "easy",
    "early": "late", "late": "early",
    "clean": "dirty", "dirty": "clean",
    "new": "old", "old": "new",
    "young": "old", "rich": "poor", "poor": "rich",
    "kind": "mean", "mean": "kind",
    "safe": "dangerous", "dangerous": "safe",
    "empty": "full", "full": "empty",
    "tall": "short", "short": "tall",
    "wide": "narrow", "narrow": "wide",
    "open": "closed", "closed": "open",
    "sharp": "dull", "dull": "sharp",
    "quiet": "loud", "loud": "quiet",
    "alive": "dead", "dead": "alive",
    "dry": "wet", "wet": "dry",
    "true": "false", "false": "true",
    "hard": "soft", "soft": "hard",
    "thick": "thin", "thin": "thick",
    "beautiful": "ugly", "ugly": "beautiful",
    "friendly": "hostile", "hostile": "friendly"
}


def slightly_wrong_numbers(text: str) -> str:
    """
    Slightly alters numeric values in the input text by ±25%.

    Args:
        text (str): A string that may contain numbers.

    Returns:
        str: The modified text with changed numeric values.
    """
    words = text.split()
    new_words = []

    for word in words:
        if word.isdigit():
            number = int(word)
            delta = int(number * 0.25)
            new_number = number + delta if number % 2 == 0 else number - delta
            new_words.append(str(new_number))
        else:
            new_words.append(word)

    return " ".join(new_words)


def opposite_attribute(text: str) -> str:
    """
    Replaces known adjectives in the input text with their opposites.

    Args:
        text (str): A sentence containing descriptive attributes.

    Returns:
        str: The sentence with swapped attributes (if found).
    """
    words = text.split()
    new_words = []

    for word in words:
        clean_word = word.lower().strip(",.!?")
        if clean_word in attribute_opposites:
            replacement = attribute_opposites[clean_word]
            if word[0].isupper():
                replacement = replacement.capitalize()
            new_words.append(replacement)
        else:
            new_words.append(word)

    return " ".join(new_words)


def flip_meaning(text: str) -> str:
    """
    Flips sentence logic by inserting negation into key verbs (is/are/was/...).

    Args:
        text (str): A declarative sentence.

    Returns:
        str: The sentence with logical negation applied.
    """
    words = text.split()
    new_words = []

    for word in words:
        lower = word.lower()
        if lower == "is":
            new_words.append("is not")
        elif lower == "are":
            new_words.append("are not")
        elif lower == "was":
            new_words.append("was not")
        elif lower == "were":
            new_words.append("were not")
        elif lower == "will":
            new_words.append("will not")
        else:
            new_words.append(word)

    return " ".join(new_words)


def generate_lie(true_fact: str) -> str:
    """
    Attempts to generate a plausible lie from a true statement using simple transformations.

    Priority:
        1. Slightly modify numbers
        2. Invert known attributes
        3. Flip sentence logic

    Args:
        true_fact (str): A factual sentence.

    Returns:
        str: A sentence that contains a fabricated element.
    """
    try:
        modified = slightly_wrong_numbers(true_fact)
        if modified != true_fact:
            return modified

        modified = opposite_attribute(true_fact)
        if modified != true_fact:
            return modified

        return flip_meaning(true_fact)

    except Exception as e:
        print(f"An error has occurred: {e}")
        return true_fact  # Fallback to original input if failure occurs
