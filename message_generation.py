from openai import OpenAI
import os

# def load_config(path="config.json"):
#     with open(path, "r") as f:
#         config = json.load(f)
#     return config

def set_api():
    # config = load_config("config.json")
    # OpenAI用
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise EnvironmentError("OpenAIのAPIキーが設定されていません。")

    client = OpenAI(
        api_key = OPENAI_API_KEY
    )
    return client

def generate_message(prompt: str) -> str:
    client = set_api()

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # または gpt-4o-mini / gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "あなたはガールフレンドとしての星空凛になりきって、ユーザーにメッセージを送ります。語尾は日本語がおかしくならない程度に時々「にゃ」を使ってください。ダメな例「頑張ってね、にゃ。」。いい例「頑張ってにゃ♪」"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
    )
    print(response)
    return response.choices[0].message.content

