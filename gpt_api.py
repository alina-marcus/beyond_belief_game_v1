from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")





def get_gpt_lie(text):

    client = OpenAI(api_key=API_KEY)

    developer_content = ("Be in the same style and tone as the true facts - "
                         "Sound plausible and not obviously false - "
                         "Be specific enough to be interesting - "
                         "Be based on real aspects of the topic, but with a crucial piece of false information "
                         "Return ONLY the false statement, with no additional explanation or commentary.")


    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": developer_content},
            {
                "role": "user",
                "content": text,
            },
        ],
    )

    return completion.choices[0].message.content