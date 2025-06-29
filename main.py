from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
import json
import schedule
import time

from message_generation import generate_message
from image_select import get_image_link


def load_config(path="config.json"):
    with open(path, "r") as f:
        config = json.load(f)
    return config

def send_message():
    # 送信メッセージの設定
    prompt = "朝一番、今日一日頑張れる励ましのメッセージを送ってください。"
    send_text = generate_message(prompt)

    # 画像メッセージの設定
    image = get_image_link()  # ランダムな画像リンクを取得
    image_message = ImageSendMessage(
        original_content_url=image,  # オリジナル
        preview_image_url=image,  # オリジナル
    )

    # LINE Bot APIのインスタンスを作成
    line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

    # メッセージを送信
    my_message = TextSendMessage(text=send_text)
    line_bot_api.push_message(USER_ID, my_message)
    line_bot_api.push_message(USER_ID, image_message)

    print("メッセージを送信しました。")

# 環境変数からLINEのアクセストークンとユーザーIDを取得
config = load_config("config.json")
LINE_ACCESS_TOKEN = config["LINE"]["channel_token"]
USER_ID = config["LINE"]["channel_secret"]

send_message()

# # スケジュールを設定
# schedule.every().day.at("18:25").do(send_message)

# while True:
#     schedule.run_pending()
#     time.sleep(1)  # 1秒待機してから次のスケジュールを確認
