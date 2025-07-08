import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


def get_gpt_lie(text: str) -> str:
    """
    Generates a plausible lie based on a given true statement.

    The lie should:
        - Match the style and tone of the original fact
        - Sound believable and not obviously false
        - Be specific and interesting
        - Be based on the real topic but include a key falsehood
        - Return only the fabricated statement with no extra explanation

    Args:
        text (str): A true factual sentence.

    Returns:
        str: A single, plausible false sentence.
    """
    client = OpenAI(api_key=API_KEY)

    developer_content = (
        "Be in the same style and tone as the true facts — "
        "Sound plausible and not obviously false — "
        "Be specific enough to be interesting — "
        "Be based on real aspects of the topic, but with a crucial piece of false information. "
        "Return ONLY the false statement, with no additional explanation or commentary."
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": developer_content},
            {"role": "user", "content": text},
        ],
    )

    return completion.choices[0].message.content.strip()
