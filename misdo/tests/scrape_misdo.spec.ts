import { test } from '@playwright/test';
import fs from 'fs';

function toCsv(items: any[]) {
  const header = [
    'name',
    'url',
    'image',
    'takeout_price',
    'eatin_price',
  ].join(',');

  const rows = items.map(item =>
  [
    item.name,
    item.url,
    item.image,
    item.takeout_price,
    item.eatin_price,
  ]
    .map(v => `"${(v ?? '').replace(/"/g, '""')}"`)
    .join(',')
  );

  return [header, ...rows].join('\n');
}

test('商品一覧ページをスクレイピングする', async ({ page }) => {
    //①　ページにアクセス
    await page.goto('https://www.misterdonut.jp/m_menu/donut/', {
        waitUntil: 'load',
    });

    //②　商品が表示されるまで待つ
        await page.waitForSelector('main');

    //③　商品一覧を取得
    const items = page.locator('li.mod_item.clm');
    const itemCount = await items.count();

    const results: any[] = [];

    for (let i = 0; i < itemCount; i++) {
        const item = items.nth(i);

        const name = (await item.locator('.txt').textContent())?.trim();
        const href = await item.locator('a').getAttribute('href');
        const img = await item.locator('.img img').getAttribute('src');
        
        const takeoutLocator = item.locator('.price_tax');
        const takeout = (await takeoutLocator.count()) > 0
         ? (await takeoutLocator.textContent())?.trim()
         : null;
        const eatinLocator = item.locator('.price_takeout');
        const eatin = (await eatinLocator.count()) > 0
         ? (await eatinLocator.textContent())?.trim()
         : null;


                results.push({
            name,
            url: href ? `https://www.misterdonut.jp${href}` : null,
            image: img,
            takeout_price: takeout,
            eatin_price: eatin,
        });
    }

    //④　結果確認
    console.log('商品数:', results.length);
    console.log(results.slice(0, 3));

    //⑤　jsonに保存
    fs.writeFileSync(
        'misdo/data/misdo_products.json',
        JSON.stringify(
            {
                count: results.length,
                item: results,
            },
            null,
            2
        ),
        'utf-8'
    );

    // csv
    const csv = toCsv(results);
    fs.writeFileSync('misdo/data/misdo_products.csv', csv, 'utf-8')
    
    //⑥　スクリーンショット
    await page.screenshot({
        path: 'misdo/images/misdo_product-list.png',
        fullPage: true,
    });
});

//});