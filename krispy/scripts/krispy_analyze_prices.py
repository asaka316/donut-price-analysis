import pandas as pd
import os
import matplotlib.pyplot as plt

# data/krispy-products.csv を読み込む
script_dir = os.path.dirname(__file__)

base_dir = os.path.dirname(script_dir)

data_dir = os.path.join(base_dir, "data")
images_dir = os.path.join(base_dir, "images")

os.makedirs(data_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

csv_path = os.path.join(data_dir, 'krispy-products.csv')
df = pd.read_csv(
    csv_path,
    encoding="utf-8-sig"
)

print("shape:", df.shape)
print(df.head())
print(df.iloc[0])

price_series = (
    df["takeoutPrice"]
    .astype(str)
    .str.extract(r"(\d+)")
    .astype(float)[0]
)

print("価格あり件数:", price_series.notna().sum())
print(price_series.head())

# ③ 基本統計
summary = price_series.describe()
summary_csv_path = os.path.join(data_dir, "krispy_products_summary.csv")
summary.to_csv(summary_csv_path)


# ④ グラフ作成
plt.figure(figsize=(8,5))
plt.hist(price_series.dropna(), bins=10)
plt.xlabel("Price (¥)")
plt.ylabel("Number of Products")
plt.title("Distribution of Takeout Prices (Krispy Kreme)")
plt.tight_layout()
plt.savefig(os.path.join(images_dir, "krispy_price_distribution.png"))
plt.show()
