from flickrapi import FlickrAPI
from urllib.request import urlretrieve
import os, time, sys

key = "00143a9bfdca7c8fc7b6c5937eff4a89" # flickrapiのキー
secret = "7104d94bd8779a5f"
wait_time = 1  # 1秒間隔でリクエストを送信してアクセスするようにする

keyword = sys.argv[1]  # 検索キーワードが１番目の引数
savedir = "./" + keyword

flickr = FlickrAPI(key, secret, format="parsed-json")
result = flickr.photos.search(
    text=keyword,
    per_page=400,
    media="photos",             # 写真
    sort="relevance",          # 最新の物から取得
    safe_search=0.1,             # 暴力的な画像を避ける
    extras = "url_q, license"  # ダウンロード用URLとライセンス
)

photos = result["photos"]

for i, photo in enumerate(photos["photo"]):
    url_q = photo["url_q"]
    file_path = savedir + "/" + photo["id"] + ".jpg"
    if os.path.exists(file_path): continue
    urlretrieve(url_q, file_path)  # URLからダウンロードして、file_pathに保存する
    time.sleep(wait_time)




