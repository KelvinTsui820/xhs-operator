const puppeteer = require('F:/order_workflow/node_modules/puppeteer-core');
const path = require('path');
const fs = require('fs');

async function renderCards() {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  if (!fs.existsSync(chromePath)) {
    console.error('Chrome not found at', chromePath);
    return;
  }

  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1200, deviceScaleFactor: 2 });

  const htmlPath = path.resolve('F:/xhs_operator/cards/post1_carousel.html');
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

  // Activate HD mode for crystal crisp output
  await page.evaluate(() => {
    document.body.classList.add('hd-mode');
  });
  await new Promise(r => setTimeout(r, 600));

  const cardsDir = path.resolve('F:/xhs_operator/cards');
  const cardConfigs = [
    { id: '#card-1', file: '01_cover_carousel.jpg' },
    { id: '#card-2', file: '02_pain_points.jpg' },
    { id: '#card-3', file: '03_excel_delivery.jpg' },
    { id: '#card-4', file: '04_community_action.jpg' }
  ];

  for (const cfg of cardConfigs) {
    const el = await page.$(cfg.id);
    if (el) {
      const outPath = path.join(cardsDir, cfg.file);
      await el.screenshot({ path: outPath, type: 'jpeg', quality: 95 });
      console.log(`✅ 已导出高清卡片: ${cfg.file}`);
    } else {
      console.warn(`⚠️ 未找到卡片节点: ${cfg.id}`);
    }
  }

  await browser.close();
  console.log('🎉 4 张 3:4 视觉手作卡片全部导出完毕！');
}

renderCards().catch(err => {
  console.error('导出失败:', err);
  process.exit(1);
});
