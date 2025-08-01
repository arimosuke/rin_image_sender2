from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
import json
import schedule
import datetime
import time
import random
import os

from message_generation import generate_message
from image_select import get_image_link

prompt_morning = "朝一番、今日一日頑張れる励ましのメッセージを送ってください。"
prompt_lunch = "お昼ご飯の後でもお仕事を頑張れるようなメッセージを送ってください。"
prompt_afternoon = "午後の仕事もあと少し、力が出るようなメッセージを送ってください。"
prompt_evening = "今日も一日お疲れ様でした。明日も頑張れるようなメッセージを送ってください。"
prompt_night = "夜遅くまでお疲れ様です。明日も良い日になりますように、励ましのメッセージを送ってください。"

# def load_config(path="config.json"):
#     with open(path, "r") as f:
#         config = json.load(f)
#     return config

def wait_random_offset(max_offset_min=5):
    delay = random.randint(0, max_offset_min *60)
    print(f"⏱ ランダム待機時間: {delay // 60}分 {delay % 60}秒")
    time.sleep(delay)
    
def get_prompt_by_time(pre_prompt=None):
    now_jst = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
    hour = now_jst.hour
    print(now_jst)
    
    # 現在時刻によってメッセージの内容を変える。
    if hour < 9:
        base_prompt = prompt_morning
    elif hour < 14:
        base_prompt = prompt_lunch
    elif hour < 18:
        base_prompt = prompt_afternoon
    elif hour < 22:
        base_prompt = prompt_evening
    else:
        base_prompt = prompt_night
        
    style_tags = [
    "甘やかす感じで",
    "恥ずかしがっている感じで",
    "ちょっとツンデレっぽく",
    "熱血応援モードで",
    "少し不安そうな感じで",
    "小悪魔っぽく誘惑しながら",
    "ゆるっと眠たそうに",
    "テンション高めでハイになって",
    "知識人っぽくアドバイス調で",
    "恋人が愛をささやく感じで"
    "元気いっぱいに"
    "心配するような感じで"
    "しょうがないな〜、という感じで"
    ]

    prompt = f"{random.choice(style_tags)}{base_prompt}"

        
    prompt = pre_prompt if pre_prompt else prompt
    
    return prompt

def send_message(pre_prompt=None):
    # 送信メッセージの設定
    if random.random() > 0.03:
        print("通常verでお届け")
        send_text = generate_message(get_prompt_by_time())
    else:
        print("特別verでお届けにゃ♪")
        pre_prompt = "恋人になりきって好きだということを伝えて"
        send_text = generate_message(get_prompt_by_time(pre_prompt))

    # 画像メッセージの設定
    image = get_image_link()  # ランダムな画像リンクを取得
    image_message = ImageSendMessage(
        original_content_url=image,  # オリジナル
        preview_image_url=image,  # オリジナル
    )
    
    wait_random_offset()

    # LINE Bot APIのインスタンスを作成
    line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

    # メッセージを送信
    my_message = TextSendMessage(text=send_text)
    line_bot_api.push_message(USER_ID, my_message)
    line_bot_api.push_message(USER_ID, image_message)

    print("メッセージを送信しました。")


# def schedule_daily_reset():
#     # 毎日0:01に、翌日の送信をランダム時刻で再スケジュール
#     schedule.every().day.at("00:01").do(schedule_next_message)

# def schedule_next_message():
#     time_slots = [
#         ("07", (0, 59)),
#         ("12", (50, 59)),
#         ("17", (0, 59)),
#         ("20", (0, 59)),
#         ("22", (0, 59)),
#     ]

#     for hour, (min_start, min_end) in time_slots:
#         minute = random.randint(min_start, min_end)
#         time_str = f"{hour}:{minute:02d}"
#         print(f"⏰ スケジュール登録: {time_str}")
#         schedule.every().day.at(time_str).do(send_message)
    
#     schedule_daily_reset()

if random.random() > 0.6:
    print("今回はスキップします")
    exit()

# # 環境変数からLINEのアクセストークンとユーザーIDを取得
# config = load_config("config.json")
# LINE_ACCESS_TOKEN = config["LINE"]["channel_token"]
# USER_ID = config["LINE"]["channel_secret"]

# github actionでAPIキーを取得するよう
# LINE用
LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
USER_ID = os.environ.get("LINE_USER_ID")



# エラーハンドリング（任意）
if not LINE_ACCESS_TOKEN or not USER_ID:
    raise EnvironmentError("LINEの環境変数が正しく設定されていません。")



send_message()

# for i in range(5):
# prompts_list = [prompt_morning, prompt_lunch, prompt_afternoon, prompt_evening, prompt_night]
# send_message(pre_prompt=random.choice(prompts_list))  # ランダムなプロンプトで初回メッセージを送信

# schedule_next_message()

# while True:
#     schedule.run_pending()
#     time.sleep(60)  # 1秒待機してから次のスケジュールを確認
