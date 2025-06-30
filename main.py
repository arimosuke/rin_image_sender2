from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
import json
import schedule
import datetime
import time
import random

from message_generation import generate_message
from image_select import get_image_link


def load_config(path="config.json"):
    with open(path, "r") as f:
        config = json.load(f)
    return config

def send_message():
    # 今の時刻を取得
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"メッセージ送信時刻: {current_time}")

    # 現在自国によってメッセージの内容を変える。
    if datetime.datetime.now().hour < 9:
        prompt = "朝一番、今日一日頑張れる励ましのメッセージを送ってください。"
    elif datetime.datetime.now().hour < 14:
        prompt = "お昼ご飯の後は眠いけど、それでもお仕事を頑張れるようなメッセージを送ってください。"
    elif datetime.datetime.now().hour < 18:
        prompt = "午後の仕事もあと少し、頑張れるようなメッセージを送ってください。"
    elif datetime.datetime.now().hour < 22:
        prompt = "今日も一日お疲れ様でした。明日も頑張れるようなメッセージを送ってください。"
    else:
        prompt = "夜遅くまでお疲れ様です。明日も良い日になりますように、励ましのメッセージを送ってください。"

    # 送信メッセージの設定
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


def schedule_daily_reset():
    # 毎日0:01に、翌日の送信をランダム時刻で再スケジュール
    schedule.every().day.at("00:01").do(schedule_next_message)

def schedule_next_message():
    time_slots = [
        ("07", (0, 59)),
        ("12", (50, 59)),
        ("17", (0, 59)),
        ("20", (0, 59)),
        ("22", (0, 59)),
    ]

    for hour, (min_start, min_end) in time_slots:
        minute = random.randint(min_start, min_end)
        time_str = f"{hour}:{minute:02d}"
        print(f"⏰ スケジュール登録: {time_str}")
        schedule.every().day.at(time_str).do(send_message)


# 環境変数からLINEのアクセストークンとユーザーIDを取得
config = load_config("config.json")
LINE_ACCESS_TOKEN = config["LINE"]["channel_token"]
USER_ID = config["LINE"]["channel_secret"]

send_message()
schedule_next_message()

while True:
    schedule.run_pending()
    time.sleep(60)  # 1秒待機してから次のスケジュールを確認
