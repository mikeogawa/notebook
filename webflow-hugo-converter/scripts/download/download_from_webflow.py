import asyncio
from playwright.async_api import async_playwright, Playwright

TARGET_PAGE = "design.webflow.com"
DOWNLOAD_PATH = "tmp/design_file.zip"

async def get_webflow_data(playwright: Playwright):
    browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
    default_context = browser.contexts[0]
    page = next(filter(lambda page: TARGET_PAGE in page.url, default_context.pages), None)
    if page is None:
        raise Exception("Webflow page not found.")

    await page.locator("[data-automation-id='top-bar-export-code-button']").click(timeout=4000)
    await page.locator("[data-automation-id='code-export-prepare-zip-button']").click(timeout=420*1000)
    async with page.expect_download() as download_info:
        await page.locator("a[download]").click()
    download = await download_info.value
    await download.save_as(DOWNLOAD_PATH)


async def main():
    async with async_playwright() as playwright:
        await get_webflow_data(playwright)

if __name__ == "__main__":
    asyncio.run(main())