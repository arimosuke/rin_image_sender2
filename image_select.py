import os
import random
import urllib.parse

folder_path = 'img'  # 画像フォルダのパス
img_url = "https://arimosuke.github.io/rin_image_sender2/"

# imgフォルダ配下の画像ファイル情報を取り込む
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            images.append(os.path.join(folder, filename))
    return images

# ランダムにどれか一つを選ぶ
def select_random_image(images):
    if images:
        return random.choice(images)
    return None

# リンクにしてアドレスを返す
def get_image_link():
    images = load_images_from_folder(folder_path)
    image = select_random_image(images)
    print(img_url + image)
    raw_url = img_url + image
    encoded_url = urllib.parse.quote(raw_url, safe=':/')
    print(encoded_url)
    return encoded_url
