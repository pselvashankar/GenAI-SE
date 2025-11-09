import time
import sys
from playwright.sync_api import sync_playwright, Playwright

# --- Prerequisites ---
# pip install playwright
# playwright install chromium

def run(p: Playwright):
    """
    Automates searching DuckDuckGo and clicking the first result.
    
    FIX 4: Uses a highly specific locator ('article[data-testid="result"] h2 a')
    to ensure only the main result title link is clicked, avoiding filter links.
    """
    
    print("Starting Chromium browser...")
    try:
        browser = p.chromium.launch(
            headless=False, 
            slow_mo=500  # Slow down execution for visibility
        )
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"})
        
    except Exception as e:
        print(f"Error launching browser: {e}")
        return

    try:
        search_query = "tnurbanepay"
        # Construct the search results URL directly
        search_url = f"https://duckduckgo.com/?q={search_query}"
        
        # 2. Navigate DIRECTLY to the Search Results
        print(f"Navigating directly to search results: {search_url}...")
        page.goto(search_url)

        # 4. Wait for Search Results & 5. Click First Link
        
        # FIX: Targeted Locator - Ensures we click the link within the <h2> tag (the result title)
        print("Waiting for main search result link... (Max 20s)")
        first_result_link = page.locator('article[data-testid="result"] h2 a').first

        # Get link info before clicking
        # Playwright will wait for the element to be visible when we try to read properties
        link_text = first_result_link.inner_text(timeout=20000)
        link_href = first_result_link.get_attribute("href")
        print(f"Clicking the first search result, titled: '{link_text}', leading to: '{link_href}'")
        
        # Click the link, Playwright implicitly waits for clickability
        first_result_link.click(timeout=30000) # Increased timeout for click robustness

        # 6. Final check and pause
        print("Waiting for navigation to complete...")
        page.wait_for_load_state("load", timeout=20000)
        
        print(f"Successfully navigated to the site: {page.url}")
        
        print("Pausing for 5 seconds before closing the browser...")
        page.wait_for_timeout(5000)

    except Exception as e:
        print(f"\nAn error occurred during execution: {e}", file=sys.stderr)
        page.screenshot(path="playwright_error.png")
        print("Saved a screenshot to 'playwright_error.png' for debugging.")
    finally:
        # 7. Close the browser
        print("Closing browser.")
        browser.close()

if __name__ == '__main__':
    with sync_playwright() as p:
        run(p)