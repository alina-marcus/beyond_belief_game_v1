import pickle
import os
import requests
import nltk
import time
import re
import random
import json

# Set NLTK data path locally
nltk.data.path.append('./data/nltk_data')
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
PATH_CATEGORY = 'data/spooky_categories.json'

MINIMUM_SENTENCE_COUNT = 3



def load_categories_from_json(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
        return data.get("categories", [])

def fetch_random_wikipedia_title():
    """Fetches a random Wikipedia page title."""
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
        print(f"Error fetching title: {e}")
        return None




def fetch_random_page_from_category(category, limit=10, retries=3, backoff_factor=1):
    """Fetches a random Wikipedia page title from a specified category."""
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

    print(f"Failed to fetch category '{category}' after {retries} attempts.")
    return None


def fetch_wikipedia_page_content(title, retries=3, backoff_factor=1):
    """Fetches the plaintext content of a Wikipedia page given its title."""
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
            print(f"Unexpected error fetching page content '{title}': {e}")
            return None

    print(f"Failed to fetch content for page '{title}' after {retries} attempts.")
    return None


def load_tokenizer():
    """Loads the NLTK Punkt tokenizer from local storage."""
    model_path = os.path.join('data/nltk_data', 'tokenizers', 'punkt', 'english.pickle')
    with open(model_path, 'rb') as f:
        return pickle.load(f)

def divide_sentences(text):
    """Tokenizes raw text into sentences."""
    tokenizer = load_tokenizer()
    return tokenizer.tokenize(text)

def clean_sentences(sentences):
    """Cleans sentences by removing Wikipedia-specific markup."""
    cleaned = []
    for s in sentences:
        s = re.sub(r'\=\=.*?\=\=', '', s)
        s = re.sub(r'\[\[|\]\]', '', s)
        s = re.sub(r'\{\{.*?\}\}', '', s)
        s = re.sub(r'<ref.*?>.*?</ref>', '', s)
        s = re.sub(r'\n', ' ', s)
        cleaned.append(s.strip())
    return cleaned

def filter_linguistically_normal_nltk(sentences):
    """Filters sentences to retain linguistically normal sentences."""
    return [s.strip() for s in sentences if len(s) >= 20 and len(s) > 300 and len(s.split()) >= 4 and not re.match(r'^[^a-zA-Z]+$', s) and not any(char in s for char in "{}[]|=*<>") and s.count('.') <= 3]

def is_sentence_appropriate(sentences):
    """Checks if the sentence count meets the minimum requirement."""
    return len(sentences) >= MINIMUM_SENTENCE_COUNT

def get_valid_wikipedia_page_info(spooky=False):
    """Fetches a valid Wikipedia page, optionally from spooky categories."""

    categories = load_categories_from_json(PATH_CATEGORY)

    while True:
        title = fetch_random_page_from_category(random.choice(categories)) if spooky else fetch_random_wikipedia_title()
        content = fetch_wikipedia_page_content(title)
        sentences = filter_linguistically_normal_nltk(clean_sentences(divide_sentences(content)))
        if is_sentence_appropriate(sentences):
            return title, sentences
        time.sleep(0.5)

if __name__ == "__main__":
    title, sentences = get_valid_wikipedia_page_info(spooky=True)
    print(f"Title: {title}")
    print(f"Sentences ({len(sentences)}):")
    for sentence in sentences:
        print(sentence)