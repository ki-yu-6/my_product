# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,session
from map import geocode, calc
import pandas as pd

app=Flask(__name__)
app.secret_key = 'drive_moto'

df=pd.read_csv('moto_spots_after.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')


@app.route('/chi', methods=['GET', 'POST'])
def choice():
  if request.method=="GET":
    return render_template('choice.html')
  elif request.method=='POST':
    if "family" in request.form:
      session['label_filter']=0
    elif "partner" in request.form:
      session['label_filter']=1
    else:
      session['label_filter']=None
    return render_template('keyword.html')

@app.route('/key', methods=['GET', 'POST'])
def keyword():
    if request.method == 'GET':
        return render_template('keyword.html')
    elif request.method == 'POST':
        keyword = request.form.get('keyword')
        others_key = request.form.get('others_key', '')

        print("受け取った keyword:", keyword)
        print("others_key の値:", others_key)

        if keyword in ["桜", "海", "川", "山", "夜景"]:
            session['key_filter'] = keyword
        elif keyword == "other" and others_key:
            session['key_filter'] = others_key
        elif keyword == "none":
            session['key_filter'] = None

        print("保存された key_filter:", session.get('key_filter'))

        return render_template('distance.html')


@app.route('/dist', methods=['GET', 'POST'])
def distance():
  results=None
  if request.method=='GET':
    return render_template('distance.html')
  elif request.method=='POST':
    address=request.form['address']
    min_dist=float(request.form['min_dist'])
    max_dist=float(request.form['max_dist'])
    try:
        user_lat, user_lng = geocode(address)
    except Exception as e:
        return render_template('distance.html', error="住所が見つかりませんでした。もう一度入力してください。")


    fil_df=df.copy()

    label_filter=session.get('label_filter')
    if label_filter is not None:
      fil_df=fil_df[fil_df['predicted_label_id']==label_filter]

    key_filter=session.get('key_filter')
    if key_filter=="桜":
      fil_df=fil_df[fil_df["introduction"].str.contains("桜", na=False) & ~fil_df["introduction"].str.contains("若桜町|黄桜|滋賀県野洲市北桜|奈良県桜井市", na=False)]
    elif key_filter=="海":
      fil_df=fil_df[fil_df["introduction"].str.contains("海", na=False) & ~fil_df["introduction"].str.contains("雲海|海津大崎|海の生き物|海洋博物館|海のない|南海電車|新長田駅を海側|海外|海南サクアス|海山|NIFREL|制海権|梅林|あわじ花さじき|塩津海道|ら～めん幕末 海南店|住吉大神|海の京都 宮津|玄武洞|ジャイアントパンダ|海鮮マーケット|水無瀬神宮|錦市場|ジオパーク浜坂の郷|花緑公園内|菩提寺|鶉野飛行場|黒壁スクエア|東寺|舟屋の里伊根|観心寺|高野山奥之院", na=False)]
    elif key_filter=="川":
      fil_df=fil_df[fil_df["introduction"].str.contains("川", na=False) & ~fil_df["introduction"].str.contains("徳川|カワサキワールド|大和川線|川崎重工|最初ヶ峰|古川鉄治郎|矢田川|生石高原|天の川|有田川町")]
    elif key_filter=="山":
      fil_df=fil_df[fil_df["introduction"].str.contains("山", na=False)]
    elif key_filter=="夜景":
      fil_df=fil_df[fil_df["introduction"].str.contains("夜景", na=False)]
    elif key_filter:
      fil_df=fil_df[fil_df["introduction"].str.contains(key_filter, na=False)]
    elif key_filter==None:
      fil_df=fil_df

    results_df=calc(user_lat, user_lng, min_dist, max_dist, fil_df)

    if not results_df.empty:
      results_df = results_df.sample(n=min(10, len(results_df)), random_state=42)
      results = results_df.to_dict(orient='records')

  return render_template('result.html', results=results)


if __name__=='__main__':
  app.run(debug=True)