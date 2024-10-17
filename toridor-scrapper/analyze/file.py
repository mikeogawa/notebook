import re
from playwright import Locator
# from playwright.sync_api import Playwright, sync_playwright, expect
from playwright.async_api import Playwright, async_playwright, expect


def run(playwright: Playwright) -> None:
    def login():
        browser = playwright.chromium.launch(headless=False)
        await browser.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://marketing.toridori.me/campaigns/85296/campaign_entries")
        page.goto("https://marketing.toridori.me/signin")
        page.get_by_label("email").fill("mike.ogawa@techmo.jp")
        page.get_by_test_id("password").fill("1234567")
        page.get_by_label("ログイン").click()
        return page

    page = login()

    def access_to_campaign():
        page.goto("https://marketing.toridori.me/campaigns/85296/campaign_entries")
        page.get_by_role("menuitem", name="キャンペーン一覧").click()
        page.locator("a.MuiCardActionArea-root").click()
        page.locator("a.MuiButtonGroup-groupedHorizontal").nth(3).click()
        return page

    page = access_to_campaign()

    def loop_per_table(page: Locator, res_list: list[dict[str, str]]):
        res_list = []
        for tr in page.locator("tbody tr").all():
            tr.click()
            page, res = on_per_page(page)
            res_list.append(res)
    
    def next_table(page: Locator) -> tuple[Locator, bool]:
        el = page.locator("button.MuiPaginationItem-root").all()[-1]
        return page, el.is_disabled()
    
    def on_per_page(locator: Locator) -> tuple[Locator, dict[str, str]]:
        locator.click()
        page.get_by_text("100").click()
        drawer_el = page.locator(".MuiPaper-root.MuiPaper-elevation.MuiDrawer-paperAnchorDockedRight")
        svg_icons = drawer_el.locator(".MuiBox-root svg").all()
        res = {}
        try:
            
            gender_icon_label = svg_icons[3].get_attribute("data-testid")
            res["gender_icon_label"] = gender_icon_label
            aria_label = svg_icons[2].get_attribute("aria-label")
            res["aria_label"] = aria_label
            followers = page.get_by_role("p", name="SNS連携").locator("..").locator("span.MuiTypography-caption").inner_text
            res["followers"] = followers
            
            icon_html = drawer_el.locator(".MuiListItemButton-root svg").evaluate("e => e.outerHTML")
            res["icon_html"] = icon_html
            name = drawer_el.locator(".MuiTypography-root.MuiTypography-h6").inner_text
            res["name"] = name
            age = drawer_el.locator(".MuiTypography-root.MuiTypography-body2").all()[1].inner_text
            res["age"] = age
            
            if not page.get_by_role("p", name="Instagramのハッシュタグ傾向").all():
                raise Exception("Instagramのハッシュタグ傾向が見つかりません")
            
            image_src = (page
                         .get_by_role("p", name="Instagramのハッシュタグ傾向")
                         .locator("..")
                         .locator("img")
                         .get_attribute("src")
                        )
            res["image_src"] = image_src

            infos_1 = drawer_el.locator(".MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-1\.5").all()
            infos_2 = drawer_el.locator(".MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-2").all()
            comments = infos_1[0].inner_text
            engagement = infos_1[1].inner_text
            likes = infos_2[0].inner_text
            res["comments"] = comments
            res["engagement"] = engagement
            res["likes"] = likes

            followers_gender = drawer_el.locator(".recharts-default-legend span[style='font-size: 1rem; font-weight: bold;']").all()
            followers_gender = [f.inner_text for f in followers_gender]

            follower_list = []
            for follower_gender in followers_gender:
                res = re.findall("[0-9]+", follower_gender)
                follower_list.append(res[0]) if res else follower_list.append("0")          
            
            for v, key in zip(follower_list, [
                "female_follower", 
                "male_follower", 
                "unknown_follower"]):
                res[key] = v

        except Exception as e:
            print(e)

        finally:
            svg_icons[0].click()
        return page, res

    for _ in range(1, 26):
        res_list = []
        page, res_list = loop_per_table(page, res_list)

        page, is_disabled = next_table(page)
        if is_disabled:
            break
    # ---------------------
    context.close()
    browser.close()


with async_playwright() as playwright:
    run(playwright)
