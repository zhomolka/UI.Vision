from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.geocaching.com/account/login")

    print("Přihlas se ručně…")
    page.wait_for_timeout(30000)  # 30 sekund na přihlášení

    context.storage_state(path="geocaching_state.json")
    print("Session uložena do geocaching_state.json")

    browser.close()
