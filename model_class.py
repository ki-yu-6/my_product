from transformers import DebertaV2Tokenizer, DebertaV2ForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# データ読み込み（CSV形式）
df = pd.read_csv("sample_class.csv")
label_map = {"子連れ家族": 0, "恋人": 1}
df["label"] = df["label"].map(label_map)

# Dataset形式に変換
dataset = Dataset.from_pandas(df)

# トークナイザーとモデル
model_name = "ku-nlp/deberta-v2-base-japanese"
tokenizer = DebertaV2Tokenizer.from_pretrained(model_name)
model = DebertaV2ForSequenceClassification.from_pretrained(model_name, num_labels=2)

# トークナイズ関数
def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True, max_length=128)

dataset = dataset.map(tokenize)

# 学習/検証用に分割（8:2）
split = dataset.train_test_split(test_size=0.2)
train_dataset = split["train"]
eval_dataset = split["test"]

# 学習設定
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    logging_dir="./logs",
    save_strategy="epoch",
)

# Trainerで学習
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer
)

trainer.train()
model.save_pretrained("./trained_model", safe_serialization=True)
tokenizer.save_pretrained("./trained_model")