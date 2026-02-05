import { test } from '@playwright/test';
import fs from 'fs';
import path from 'path';

test('クリスピー 一覧URL取得→JSON保存', async ({ page }) => {
  await page.goto('https://krispykreme.jp/menu/cat/doughnuts/', {
    waitUntil: 'networkidle',
  });

  // 商品カードが全部出るのを待つ
  await page.waitForSelector('.item_name_ja');

  const names = await page.locator('.item_name_ja').allTextContents();
  const urls = await page.locator('ul.menu_list li a').evaluateAll(
    links => links.map(a => a.href)
  );

  const results = names.map((name, i) => ({
    name: name.trim(),
    url: urls[i],
  })).filter(item => item.url?.includes('/menu/doughnuts/'));

  const dataDir = path.join(__dirname, '../data');
  fs.mkdirSync(dataDir, { recursive: true});

  fs.writeFileSync(
    path.join(dataDir, 'krispy_list.json'),
    JSON.stringify(results, null, 2),
    'utf-8'
  );

  console.log('保存件数:', results.length);
});


