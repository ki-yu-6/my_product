# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from map import geocode, calc
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('moto_spots_after.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/chi', methods=['GET', 'POST'])
def choice():
    if request.method == 'POST':
        if "family" in request.form:
            label_filter = 0
        elif "partner" in request.form:
            label_filter = 1
        else:
            label_filter = None
        return render_template('keyword.html', label_filter=label_filter)
    return render_template('choice.html')

@app.route('/key', methods=['GET', 'POST'])
def keyword():
    if request.method == 'POST':
        label_filter = request.form.get('label_filter')
        keyword = request.form.get('keyword')
        others_key = request.form.get('others_key', '')

        # 優先順: keyword → others_key → None
        if keyword in ["桜", "海", "川", "山", "夜景"]:
            key_filter = keyword
        elif others_key:
            key_filter = others_key
        else:
            key_filter = None

        return render_template('distance.html', label_filter=label_filter, key_filter=key_filter)
    return render_template('keyword.html')

@app.route('/dist', methods=['GET', 'POST'])
def distance():
    results = None
    if request.method == 'POST':
        label_filter = request.form.get('label_filter')
        key_filter = request.form.get('key_filter')
        address = request.form['address']
        min_dist = float(request.form['min_dist'])
        max_dist = float(request.form['max_dist'])

        try:
            user_lat, user_lng = geocode(address)
        except Exception:
            return render_template('distance.html', error="住所が見つかりませんでした。", label_filter=label_filter, key_filter=key_filter)

        fil_df = df.copy()

        if label_filter and label_filter.isdigit():
            fil_df = fil_df[fil_df['predicted_label_id'] == int(label_filter)]

        # キーワードでフィルタ
        if key_filter == "桜":
            fil_df = fil_df[fil_df["introduction"].str.contains("桜", na=False) & ~fil_df["introduction"].str.contains("若桜町|黄桜|滋賀県野洲市北桜|奈良県桜井市", na=False)]
        elif key_filter == "海":
            fil_df = fil_df[fil_df["introduction"].str.contains("海", na=False) & ~fil_df["introduction"].str.contains("雲海|海津大崎|海の生き物|海洋博物館|海のない|南海電車|新長田駅を海側|海外|海南サクアス|海山|NIFREL|制海権|梅林|あわじ花さじき|塩津海道|ら～めん幕末 海南店|住吉大神|海の京都 宮津|玄武洞|ジャイアントパンダ|海鮮マーケット|水無瀬神宮|錦市場|ジオパーク浜坂の郷|花緑公園内|菩提寺|鶉野飛行場|黒壁スクエア|東寺|舟屋の里伊根|観心寺|高野山奥之院", na=False)]
        elif key_filter == "川":
            fil_df = fil_df[fil_df["introduction"].str.contains("川", na=False) & ~fil_df["introduction"].str.contains("徳川|カワサキワールド|大和川線|川崎重工|最初ヶ峰|古川鉄治郎|矢田川|生石高原|天の川|有田川町", na=False)]
        elif key_filter == "山":
            fil_df = fil_df[fil_df["introduction"].str.contains("山", na=False)]
        elif key_filter == "夜景":
            fil_df = fil_df[fil_df["introduction"].str.contains("夜景", na=False)]
        elif key_filter:
            fil_df = fil_df[fil_df["introduction"].str.contains(key_filter, na=False)]

        results_df = calc(user_lat, user_lng, min_dist, max_dist, fil_df)

        if not results_df.empty:
            results_df = results_df.sample(n=min(10, len(results_df)), random_state=42)
            results = results_df.to_dict(orient='records')

        return render_template('result.html', results=results)
    return render_template('distance.html')


if __name__=='__main__':
  app.run(debug=True)