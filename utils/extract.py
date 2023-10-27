from playwright.sync_api import sync_playwright

def extract_full_body_html(from_url, wait_for = None):
    with sync_playwright() as p:
        TIMEOUT = 30000
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(from_url)
        page.wait_for_load_state("networkidle", timeout=TIMEOUT)
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")
        # page.wait_for_load_state('load', timeout=TIMEOUT)
        page.wait_for_timeout(3000)

        if wait_for:
            page.wait_for_selector(wait_for, timeout=TIMEOUT)
        # page.screenshot(path='steam.png', full_page=True)

        html = page.inner_html('body')

        return html
    