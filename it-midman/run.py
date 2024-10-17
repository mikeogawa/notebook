import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("about:blank")
    page.goto("chrome-error://chromewebdata/")
    page.goto("https://comperu.jp/library/business-matchingsite/")
    page.get_by_role("heading", name="２．アイミツ").click()
    page.locator("table").filter(has_text="料金プラン 月額費用：30,000円〜100,000").click()
    page.get_by_role("heading", name="３．比較ビズ").click()
    page.get_by_text("専任の営業担当や、自社でリスティング広告を行うよりも少額で始められることをウリにしています。業者探し系サイトの中では最も知名度が高いサイトと言っても過言ではあり").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
