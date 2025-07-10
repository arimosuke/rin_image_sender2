from openai import OpenAI
import json

def load_config(path="config.json"):
    with open(path, "r") as f:
        config = json.load(f)
    return config

def set_api():
    config = load_config("config.json")
    client = OpenAI(
        api_key = config["OPENAI"]["api_key"]
    )
    return client

def generate_message(prompt: str) -> str:
    client = set_api()

    response = client.responses.create(
        model="gpt-4o-mini",  # または "gpt-3.5-turbo"
        instructions="あなたはガールフレンドとしての星空凛になりきって、ユーザーにメッセージを送ります。語尾は日本語がおかしくならない程度に時々「にゃ」を使ってください。ダメな例「頑張ってね、にゃ。」。いい例「頑張ってにゃ♪」",
        input=prompt,
        temperature=0.9  # 創造性を出すには少し高め
    )
    return response.output_text
