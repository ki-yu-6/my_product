import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv

BASE_URL = "https://motospot.jp"
URL_TEMPLATE = "https://motospot.jp/search/?os=1&pi=24,25,26,27,28,29,30&sort=drecom&pg={page}"

# 各スポットのリンクを取得
def get_spot_links(soup):
    cards = soup.select('a.spot-image-link')
    spot_urls = []
    for card in cards:
        link = card.get('href')
        if link:
            spot_urls.append(urljoin(BASE_URL, link))
    return spot_urls

# スポットの詳細情報をパース（辞書で返す）
def parse_spot_detail(spot_url):
    res = requests.get(spot_url)
    soup = BeautifulSoup(res.content, "html.parser")

    def safe_select_text(selector):
        tag = soup.select_one(selector)
        return tag.get_text(strip=True) if tag else None

    spot_name = safe_select_text('div.spot-header-title-div h1')

    # ギャラリー画像を最大3枚取得
    gallery_images = []
    for img_tag in soup.select('img.spotMainImg')[:3]:
        src = img_tag.get('src')
        if src:
            gallery_images.append(urljoin(BASE_URL, src))

    introduction = safe_select_text('p[style*="margin-bottom: 15px; font-size: 0.9rem;"]')

    table = soup.select('table.spot-table tbody tr')
    address = table[0].select_one('td:nth-of-type(1)').get_text(strip=True) if len(table) > 0 else None
    traffic_jam = table[0].select_one('td:nth-of-type(2)').get_text(strip=True) if len(table) > 0 else None
    parking_area = table[1].select_one('td:nth-of-type(1)').get_text(strip=True) if len(table) > 1 else None
    best_season = table[1].select_one('td:nth-of-type(2)').get_text(strip=True) if len(table) > 1 else None
    average_budget = table[2].select_one('td:nth-of-type(1)').get_text(strip=True) if len(table) > 2 else None
    best_num = table[2].select_one('td:nth-of-type(2)').get_text(strip=True) if len(table) > 2 else None
    crowd = table[3].select_one('td:nth-of-type(1)').get_text(strip=True) if len(table) > 3 else None
    facility = table[3].select_one('td:nth-of-type(2)').get_text(strip=True) if len(table) > 3 else None

    return {
        'spot_name': spot_name,
        'gallery_images': ', '.join(gallery_images),  # リストを文字列に変換
        'introduction': introduction,
        'address': address,
        'traffic_jam': traffic_jam,
        'parking_area': parking_area,
        'best_season': best_season,
        'average_budget': average_budget,
        'best_num': best_num,
        'crowd': crowd,
        'facility': facility
    }

# メイン処理：ページを巡回してデータ収集＆CSV出力
def crawl_pages(start_page=1, end_page=3, output_csv="moto_spots.csv"):
    all_data = []

    for page_num in range(start_page, end_page + 1):
        page_url = URL_TEMPLATE.format(page=page_num)
        print(f"🌀 Fetching page {page_num}: {page_url}")
        
        res = requests.get(page_url)
        if res.status_code != 200:
            print(f"⚠️ Failed to fetch page {page_num}")
            continue

        soup = BeautifulSoup(res.content, "html.parser")
        spot_urls = get_spot_links(soup)

        for url in spot_urls:
            print(f"🔍 Scraping: {url}")
            data = parse_spot_detail(url)
            all_data.append(data)
            time.sleep(1)

        time.sleep(1)

    # CSV出力
    if all_data:
        keys = all_data[0].keys()
        with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_data)

        print(f"✅ CSVファイルに保存完了: {output_csv}")
    else:
        print("⚠️ データが収集できませんでした。")

# 実行（ページ1〜22）
crawl_pages(start_page=1, end_page=22)