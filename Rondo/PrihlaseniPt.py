from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.rondo.cz/tree/")
    print("Přihlas se ručně a klikni Resume v Inspectoru")
    page.pause()  # počká, dokud neklikneš Resume

    context.storage_state(path="rondo_state.json")
    print("Session uložena do rondo_state.json")
