from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright


def get_page_html_content(url: str) -> str:
  with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="domcontentloaded")
    return page.content()
  

async def async_get_page_html_content(url: str) -> str:
  async with async_playwright() as pw:
    browser = await pw.chromium.launch(headless=True)
    page = await browser.new_page()
    await page.goto(url, wait_until="domcontentloaded")
    html_content =  await page.content()
    return html_content