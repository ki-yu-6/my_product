import pandas as pd
# from transformers import DebertaV2Tokenizer, DebertaV2ForSequenceClassification
# import torch

# # 推論用デバイス
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # モデルとトークナイザーの読み込み
# model_dir = "./trained_model"
# tokenizer = DebertaV2Tokenizer.from_pretrained(model_dir)
# model = DebertaV2ForSequenceClassification.from_pretrained(model_dir)
# model.to(device)
# model.eval()

# # ラベル逆引きマッピング
# id2label = {0: "子連れ家族", 1: "恋人"}

# # 推論対象データの読み込み
# df = pd.read_csv("moto_spots_added.csv")

# # トークナイズ
# encodings = tokenizer(
#     list(df["introduction"]), 
#     padding=True, 
#     truncation=True, 
#     max_length=128, 
#     return_tensors="pt"
# )

# # モデルに入力を渡す
# with torch.no_grad():
#     input_ids = encodings["input_ids"].to(device)
#     attention_mask = encodings["attention_mask"].to(device)
#     outputs = model(input_ids=input_ids, attention_mask=attention_mask)
#     preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()

# # 予測ラベルをDataFrameに追加
# df["predicted_label_id"] = preds
# df["predicted_label"] = df["predicted_label_id"].map(id2label)

df=pd.read_csv("moto_spots_revised.csv")

load_station=df['introduction'].str.contains("道の駅", na=False)

df.loc[load_station, "predicted_label_id"]=2
df.loc[load_station, "predicted_label"]="道の駅"

# 結果をCSVに保存
df.to_csv("moto_spots_after.csv", index=False)

print("予測完了。")
