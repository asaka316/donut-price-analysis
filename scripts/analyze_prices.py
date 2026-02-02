import pandas as pd
import os
import matplotlib.pyplot as plt

# scripts フォルダ内の data/products.csv を読み込む
script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, "data")
images_dir = os.path.join(script_dir, "images")

csv_path = os.path.join(script_dir, 'data/products.csv')
df = pd.read_csv(csv_path)

# ② 価格を数値に変換（テイクアウトのみ）
df["takeout_price"] = df["takeout_price"].str.replace(r"[^0-9]", "", regex=True).astype(float)

# ③ 基本統計（テイクアウト主軸）
summary = df[["takeout_price"]].describe()

summary_csv_path = os.path.join(data_dir, "products_summary.csv")
summary.to_csv(summary_csv_path)  # ExcelでもOK: df.to_excel()

# ④ グラフ作成
plt.figure(figsize=(8,5))
plt.hist(df["takeout_price"], bins=10)
plt.xlabel("Price (¥)")
plt.ylabel("Number of Products")
plt.title("Distribution of Takeout Prices (Mister Donut)")
plt.tight_layout()
plt.savefig(os.path.join(images_dir, "price_distribution.png"))
plt.show()
