import pandas as pd
import os
import matplotlib.pyplot as plt

# scripts フォルダ内の data/products.csv を読み込む
script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, "data")
images_dir = os.path.join(script_dir, "images")

csv_path = os.path.join(script_dir, 'data/products.csv')
df = pd.read_csv(csv_path)

# ② 価格を数値に変換
df["takeout_price"] = df["takeout_price"].str.replace(r"[^0-9]", "", regex=True).astype(float)
df["eatin_price"] = df["eatin_price"].str.replace(r"[^0-9]", "", regex=True).astype(float)

# ③ 基本統計（最安・平均・最大）
summary = df[["takeout_price","eatin_price"]].describe()

summary_csv_path = os.path.join(data_dir, "products_summary.csv")
summary.to_csv(summary_csv_path)  # ExcelでもOK: df.to_excel()

# ④ グラフ作成
plt.figure(figsize=(12,6))
plt.bar(df["name"], df["takeout_price"], color="skyblue", label="Takeout")
plt.bar(df["name"], df["eatin_price"], color="orange", alpha=0.5, label="Eatin")
plt.xticks(rotation=90)
plt.ylabel("Price (¥)")
plt.title("Mister Donut: Takeout vs Eatin Prices")
plt.legend()
plt.tight_layout()
plt.savefig("images/price_diff.png")
plt.show()
