import os
import pickle
import json
import time
import random
import re
import requests
import nltk

# Constants
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
NLTK_DATA_PATH = './data/nltk_data'
PUNKT_MODEL_PATH = os.path.join(NLTK_DATA_PATH, 'tokenizers', 'punkt', 'english.pickle')
CATEGORY_JSON_PATH = 'data/spooky_categories.json'
MINIMUM_SENTENCE_COUNT = 3
MIN_SENTENCE_LENGTH = 100

# Ensure NLTK uses the local data path
nltk.data.path.append(NLTK_DATA_PATH)


def load_categories_from_json(filepath):
    """
    Loads a list of categories from a JSON file.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        list: List of category names.
    """
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data.get("categories", [])


def fetch_random_wikipedia_title():
    """
    Fetches a random Wikipedia article title.

    Returns:
        str | None: Title string or None on failure.
    """
    try:
        params = {
            "action": "query",
            "list": "random",
            "rnlimit": 1,
            "rnnamespace": 0,
            "format": "json"
        }
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        return response.json()["query"]["random"][0]["title"]
    except Exception as e:
        print(f"Error fetching random title: {e}")
        return None


def fetch_random_page_from_category(category, limit=10, retries=3, backoff_factor=1):
    """
    Fetches a random page title from a specific Wikipedia category.

    Args:
        category (str): Category name.
        limit (int): Number of pages to fetch.
        retries (int): Number of retry attempts on failure.
        backoff_factor (float): Time multiplier for exponential backoff.

    Returns:
        str | None: Random page title or None if failed.
    """
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": limit,
        "cmtype": "page",
        "format": "json"
    }

    for attempt in range(retries):
        try:
            response = requests.get(WIKIPEDIA_API_URL, params=params, timeout=10)
            response.raise_for_status()
            members = response.json().get("query", {}).get("categorymembers", [])
            if not members:
                print(f"No pages found in category: {category}")
                return None
            return random.choice(members)["title"]
        except requests.RequestException as e:
            wait_time = backoff_factor * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time:.1f}s...")
            time.sleep(wait_time)

    print(f"Failed to fetch from category '{category}' after {retries} attempts.")
    return None


def fetch_wikipedia_page_content(title, retries=3, backoff_factor=1):
    """
    Fetches plaintext content of a Wikipedia page.

    Args:
        title (str): Wikipedia article title.
        retries (int): Retry attempts on failure.
        backoff_factor (float): Backoff multiplier for delay.

    Returns:
        str | None: Plaintext content or None if failed.
    """
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
        "format": "json"
    }

    for attempt in range(retries):
        try:
            response = requests.get(WIKIPEDIA_API_URL, params=params, timeout=10)
            response.raise_for_status()
            pages = response.json().get("query", {}).get("pages", {})
            return next(iter(pages.values())).get("extract", "")
        except requests.RequestException as e:
            wait_time = backoff_factor * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time:.1f}s...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Unexpected error fetching '{title}': {e}")
            return None

    print(f"Failed to fetch content for page '{title}' after {retries} attempts.")
    return None


def load_tokenizer():
    """
    Loads the NLTK Punkt tokenizer from local storage.

    Returns:
        PunktSentenceTokenizer: Loaded tokenizer object.
    """
    with open(PUNKT_MODEL_PATH, 'rb') as f:
        return pickle.load(f)


def divide_sentences(text):
    """
    Splits text into sentences using the Punkt tokenizer.

    Args:
        text (str): Input text.

    Returns:
        list: List of sentence strings.
    """
    tokenizer = load_tokenizer()
    return tokenizer.tokenize(text)


def clean_sentences(sentences):
    """
    Removes Wikipedia-specific markup and artifacts from sentences.

    Args:
        sentences (list): Raw sentence list.

    Returns:
        list: Cleaned sentence list.
    """
    cleaned = []
    for s in sentences:
        s = re.sub(r'\=\=.*?\=\=', '', s)
        s = re.sub(r'\[\[|\]\]', '', s)
        s = re.sub(r'\{\{.*?\}\}', '', s)
        s = re.sub(r'<ref.*?>.*?</ref>', '', s)
        s = s.replace('\n', ' ')
        cleaned.append(s.strip())
    return cleaned


def filter_linguistically_normal_nltk(sentences):
    """
    Filters out malformed, short, or unusual sentences.

    Args:
        sentences (list): List of cleaned sentences.

    Returns:
        list: Filtered sentence list.
    """
    return [
        s.strip() for s in sentences
        if len(s) > MIN_SENTENCE_LENGTH
           and len(s.split()) >= 4
           and not re.match(r'^[^a-zA-Z]+$', s)
           and not any(char in s for char in "{}[]|=*<>")
           and s.count('.') <= 3
    ]


def is_sentence_appropriate(sentences):
    """
    Validates if the number of sentences meets the minimum.

    Args:
        sentences (list): Filtered sentence list.

    Returns:
        bool: True if valid, False otherwise.
    """
    return len(sentences) >= MINIMUM_SENTENCE_COUNT


def get_valid_wikipedia_page_info(spooky=False):
    """
    Fetches a valid Wikipedia page and its content, optionally from a spooky category.

    Args:
        spooky (bool): If True, uses spooky categories.

    Returns:
        tuple: (title, list of sentences)
    """
    categories = load_categories_from_json(CATEGORY_JSON_PATH) if spooky else []

    while True:
        title = (
            fetch_random_page_from_category(random.choice(categories))
            if spooky else fetch_random_wikipedia_title()
        )

        if not title:
            continue

        content = fetch_wikipedia_page_content(title)
        if not content:
            continue

        sentences = divide_sentences(content)
        sentences = clean_sentences(sentences)
        sentences = filter_linguistically_normal_nltk(sentences)

        if is_sentence_appropriate(sentences):
            return title, sentences

        time.sleep(0.5)


if __name__ == "__main__":
    title, sentences = get_valid_wikipedia_page_info(spooky=True)
    print(f"Title: {title}")
    print(f"Sentences ({len(sentences)}):")
    for sentence in sentences:
        print(sentence)
