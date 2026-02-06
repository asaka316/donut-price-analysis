import os
import pandas as pd
import matplotlib.pyplot as plt

# ===== パス設定 =====
script_dir = os.path.dirname(__file__)
project_root = os.path.dirname(os.path.dirname(script_dir))

misdo_csv = os.path.join(project_root, "misdo", "data", "misdo_products.csv")
krispy_csv = os.path.join(project_root, "krispy", "data", "krispy-products.csv")

images_dir = os.path.join(project_root, "compare", "images")
os.makedirs(images_dir, exist_ok=True)

# ===== CSV 読み込み =====
misdo_df = pd.read_csv(misdo_csv).rename(
    columns={"takeout_price": "takeoutPrice"}
)

krispy_df = pd.read_csv(
    krispy_csv,
    header=None,
    names=["name", "url", "takeoutPrice"]
)
# ===== 価格を数値に変換 =====
def to_price(series):
    return (
        series
        .astype(str)
        .str.replace(r"[^0-9]", "", regex=True)
        .replace("", pd.NA)
        .astype(float)
        .dropna()
    )

misdo_prices = to_price(misdo_df["takeoutPrice"])
krispy_prices = to_price(krispy_df["takeoutPrice"])

print("misdo価格件数:", len(misdo_prices))
print("krispy価格件数:", len(krispy_prices))

# ===== グラフ =====
plt.figure(figsize=(8,5))
plt.hist(misdo_prices, bins=10, alpha=0.6, label="Mister Donut")
plt.hist(krispy_prices, bins=10, alpha=0.6, label="Krispy Kreme")

plt.xlabel("Price (¥)")
plt.ylabel("Number of Products")
plt.title("Takeout Price Distribution Comparison")
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(images_dir, "price_comparison_hist.png"))
plt.show()

plt.figure(figsize=(8,5))
plt.hist(misdo_prices, bins=10, alpha=0.6, label="Mister Donut")
plt.hist(krispy_prices, bins=10, alpha=0.6, label="Krispy Kreme")

plt.xlabel("Price (¥)")
plt.ylabel("Number of Products")
plt.title("Takeout Price Distribution")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(images_dir, "price_distribution_compare.png"))
plt.show()

plt.figure(figsize=(6,5))
plt.boxplot(
    [misdo_prices, krispy_prices],
    labels=["Mister Donut", "Krispy Kreme"]
)
plt.ylabel("Price (¥)")
plt.title("Price Range Comparison")
plt.tight_layout()
plt.savefig(os.path.join(images_dir, "price_boxplot.png"))
plt.show()

summary = pd.DataFrame({
    "Mister Donut": misdo_prices.describe(),
    "Krispy Kreme": krispy_prices.describe()
})

summary.to_csv(os.path.join(images_dir, "price_summary.csv"))
print(summary)
