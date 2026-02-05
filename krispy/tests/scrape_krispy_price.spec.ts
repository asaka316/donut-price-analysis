import { test } from '@playwright/test';
import fs from 'fs';
import path from 'path';

function toCsv(items: any[]) {
  const header = [
    'name',
    'url',
    'takeoutPrice',
  ].join(',');

  const rows = items.map(item =>
  [
    item.name,
    item.url,
    item.takeoutPrice,
  ]
    .map(v => `"${(v ?? '').replace(/"/g, '""')}"`)
    .join(',')
  );

  return [header, ...rows].join('\n');
}

test.setTimeout(120_000);

test('クリスピー 詳細ページ → テイクアウト価格取得（null対応）', async ({ page }) => {
  const dataDir = path.join(__dirname, '../data');
  const listPath = path.join(dataDir, 'krispy_list.json');

  const items: { name: string; url: string }[] =
    JSON.parse(fs.readFileSync(listPath, 'utf-8'));

  const results = [];

  for (const item of items) {
  if (!item.url.includes('/menu/doughnuts/')) {
    console.log('スキップ（単品以外）:', item.url);
    continue;
  }

  try {
    await page.goto(item.url, { waitUntil: 'domcontentloaded', timeout: 15000 });

    const priceLocator = page.locator('p.item_price_takeout');
    const takeoutPrice =
      (await priceLocator.count()) > 0
        ? (await priceLocator.textContent())?.trim() ?? null
        : null;

    results.push({
      name: item.name,
      url: item.url,
      takeoutPrice,
    });

  } catch (e) {
    console.log('取得失敗:', item.url);
    results.push({
      name: item.name,
      url: item.url,
      takeoutPrice: null,
    });
  }
}

  fs.writeFileSync(
    path.join(dataDir, 'krispy_products_partial.json'),
    JSON.stringify(results, null, 2),
    'utf-8'
  );
  
  const csv = toCsv(results);
  fs.writeFileSync(
    path.join(dataDir,'krispy-products.csv'),
     csv, 
     'utf-8'
    );
  
  await page.screenshot({
    path: 'krispy/images/krispy-product-list.png',
    fullPage: true,
  
  });
});
