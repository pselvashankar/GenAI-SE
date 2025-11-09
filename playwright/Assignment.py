import time
import sys
from playwright.sync_api import sync_playwright, Playwright

# --- Prerequisites ---
# pip install playwright
# playwright install chromium

def run(p: Playwright):
    """
    Automates searching DuckDuckGo, navigating to the first result, 
    and saving the final page's HTML source code to a text file.
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
        
        # 1. Navigate DIRECTLY to the Search Results
        print(f"Navigating directly to search results: {search_url}...")
        page.goto(search_url)

        # 2. Click the First Link (Using the stable locator)
        print("Waiting for main search result link...")
        # Targets the primary link within the <h2> tag inside the result article
        first_result_link = page.locator('article[data-testid="result"] h2 a').first

        # Get link info before clicking
        link_text = first_result_link.inner_text(timeout=20000)
        link_href = first_result_link.get_attribute("href")
        print(f"Clicking the first search result, titled: '{link_text}'")
        
        # Click the link and wait for the new page to load
        first_result_link.click(timeout=30000) 
        page.wait_for_load_state("load", timeout=20000)
        
        # 3. Extract and Save Source Code
        print(f"Successfully navigated to target site: {page.url}")
        
        # Get the full HTML content of the page
        print("Fetching page content...")
        html_content = page.content()
        
        output_filename = "tnurbanepay_frontend_source.txt"
        
        # Write the content to a text file
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"✅ Source code successfully saved to: **{output_filename}**")
        
        # 4. Final pause (Removed the long pause since the file is saved quickly)
        print("Pausing for 2 seconds before closing the browser...")
        page.wait_for_timeout(2000)

    except Exception as e:
        print(f"\nAn error occurred during execution: {e}", file=sys.stderr)
        page.screenshot(path="playwright_error.png")
        print("Saved a screenshot to 'playwright_error.png' for debugging.")
    finally:
        # 5. Close the browser
        print("Closing browser.")
        browser.close()

if __name__ == '__main__':
    with sync_playwright() as p:
        run(p)