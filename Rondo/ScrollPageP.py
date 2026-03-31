from playwright.sync_api import sync_playwright
import time

GC_CODE = "GC7B9D5"
LISTING_URL = f"https://www.geocaching.com/geocache/{GC_CODE}"

def extract_years(page):
    dates = page.locator(".LogDate").all_text_contents()
    years = []
    for d in dates:
        parts = d.strip().split("/")
        if len(parts) == 3:
            try:
                years.append(int(parts[2]))
            except:
                pass
    return years

def find_publish_listing(page):
    publish = page.locator("img[title='Publish Listing']")
    if publish.count() == 0:
        return None
    row = publish.first.locator("xpath=ancestor::tr")
    return row.inner_text()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    # 🔥 použijeme tvoji uloženou session
    context = browser.new_context(storage_state="geocaching_state.json")

    page = context.new_page()

    print("Otevírám listing…")
    page.goto(LISTING_URL)

    # 🔥 klikneme na tlačítko 'View all logs' přes stabilní ID
    print("Klikám na 'View all logs'…")
    page.locator("#ctl00_ContentBody_uxLogbookLink").click(timeout=15000)

    # 🔥 vypneme pointer events, aby Playwright NIKDY neklikl na 'Log a new visit'
    page.add_style_tag(content="""
        * {
            pointer-events: none !important;
        }
    """)

    time.sleep(2)

    print("Začínám scrollovat a načítat logy…")

    last_height = 0
    target_year = 2017
    found = False

    for i in range(300):
        page.evaluate("window.scrollBy(0, 3000)")
        time.sleep(1.2)

        years = extract_years(page)
        if years:
            print("Nejstarší rok zatím:", min(years))

        if years and min(years) <= target_year:
            found = True
            break

        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            print("Další logy se už nenačítají.")
            break
        last_height = new_height

    if not found:
        print("Nepodařilo se dostat k roku 2017.")
    else:
        print("Hledám Publish Listing…")
        result = find_publish_listing(page)
        if result:
            print("\n=== NALEZENO ===")
            print(result)
        else:
            print("Publish Listing nebyl nalezen.")

    browser.close()
