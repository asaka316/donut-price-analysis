# Mister Donut 価格分析
# 超初心者が大好きなドーナツで初のポートフォリオを作る

## 目的
- Playwrightでスクレイピングし、ミスドのドーナツ価格（テイクアウト/イートイン）を取得
- Pythonで分析して最安・平均・価格帯を算出
- グラフ化して可視化

## 使用技術
- Node.js / Playwright: スクレイピング
- Python / pandas / matplotlib / openpyxl: 分析・可視化
- GitHub: ポートフォリオ公開

## 成果物
- CSV/Excel: 商品一覧と統計
- 画像: スクショと価格比較グラフ
![Price Diff](images/price_diff.png)

## 実行手順
1. `npm install` で Playwright 環境を準備
2. `npx playwright test scripts/scrape_misdo.spec.ts` で CSV とスクショ作成
3. `python scripts/analyze_prices.py` で分析・グラフ作成
