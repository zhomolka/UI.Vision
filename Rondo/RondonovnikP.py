from playwright.sync_api import sync_playwright
import json

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False)
        context = browser.new_context()

        # Načteme cookies
        with open("cookies.json", "r", encoding="utf-8") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)

        # Otevřeme stránku stromu přímo v ovládaném okně
        page = context.new_page()
        page.goto("https://www.rondo.cz/tree")

        print("Čekám na iframe s hrou...")

        # Najdeme iframe s hrou
        frame = None
        for _ in range(60):
            for f in page.frames:
                if "rondonovnik" in f.url:
                    frame = f
                    break
            if frame:
                break
            page.wait_for_timeout(1000)

        if not frame:
            print("Iframe s hrou se neobjevil.")
            return

        canvas = frame.locator("canvas")
        canvas.wait_for()

        box = canvas.bounding_box()

        def click_rel(cx, cy):
            canvas.click(position={
                "x": box["width"] * cx,
                "y": box["height"] * cy
            })

        click_rel(0.15, 0.92)
        click_rel(0.32, 0.92)
        click_rel(0.50, 0.92)
        click_rel(0.68, 0.92)

        

        print("Hotovo.")
        page.wait_for_timeout(3000)

if __name__ == "__main__":
    main()
