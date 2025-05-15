import pandas as pd

df=pd.read_csv('moto_spots.csv')

#キーワード検索
def recommend1(df):
  original_df = df.copy()
  while True:
    keyword=input('キーワードを入力してください')
    if keyword:
      filter_df=df[df['introduction'].str.contains(keyword, case=False, na=False) | df['spot_name'].str.contains(keyword, case=False, na=False)]
      if not filter_df.empty:
        return filter_df
      else:
        return original_df
    else:
      print("正しく入力してください")


#誰と行くか
def choice(df):
  while True:
    if who=='家族':
      df=df[df['traffic_jam'].str.contains('普通|空いている', na=False)]
      return df
    elif who=='恋人':
      df=df[df['introduction'].str.contains('夜景|雰囲気|景色|砂浜', na=False)]
      return df
    elif who=='友達':
      df
      return df
    else:
      print('正しく回答してください')
  

  #距離
