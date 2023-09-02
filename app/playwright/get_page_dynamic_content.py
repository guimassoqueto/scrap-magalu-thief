from playwright.sync_api import sync_playwright


def get_page_html_content(url: str) -> str:
  with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="domcontentloaded")
    return page.content()