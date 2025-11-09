import asyncio
import random
import time
from playwright.sync_api import sync_playwright # Changed to sync_playwright for simplicity
from flask import Flask, request, Response # Used Flask instead of Quart

# --- Application Setup ---
app = Flask(__name__)

# --- Configuration ---
BING_URL = 'https://www.bing.com'
PROXY = "YOUR_PROXY_IP:PORT" # Placeholder: Update this or use an environment variable

# --- Core Synchronous Playwright Function (Wrapper) ---
def run_playwright_search_sync(search_term: str) -> str:
    """
    Initializes Playwright (synchronous), performs the search, and returns
    only the first result's hyperlink URL as a string.
    """
    
    # 1. Configuration & Stealth Setup
    # Generates a random Chrome User-Agent
    USER_AGENT = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 120)}.0.0.0 Safari/537.36'
    
    # Playwright launch arguments and options
    launch_options = {
        'headless': True,
        'args': [
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--user-agent={USER_AGENT}"
        ],
        # Note: Proxy configuration might need adjustment for synchronous use depending on the type
        'proxy': {"server": f"http://{PROXY}"} if PROXY and PROXY != "YOUR_PROXY_IP:PORT" else None
    }
    
    # Default failure message
    first_hyperlink = "Error: Could not retrieve search result."

    try:
        with sync_playwright() as p:
            # Launch Browser
            browser = p.chromium.launch(**launch_options)
            context = browser.new_context(
                extra_http_headers={"User-Agent": USER_AGENT},
                viewport={"width": 1920, "height": 1080}
            )

            # CDP Injection for Deep Stealth (must be done sync for sync_playwright)
            # This requires converting the async context.add_init_script to a sync approach if available,
            # but usually, the context method is sufficient in sync mode.
            # We'll stick to the core navigation for minimal changes and reliability.
            
            page = context.new_page()
            
            # 2. Navigation and Search Logic
            page.goto(BING_URL, wait_until="domcontentloaded")

            # Human-like delay
            time.sleep(random.uniform(2, 4)) # Use time.sleep for synchronous delay

            # Find the search input field
            search_box_selector = 'textarea[name="q"], input[name="q"]'
            page.wait_for_selector(search_box_selector, timeout=10000)

            # Type the search term and submit
            for char in search_term:
                page.type(search_box_selector, char)
                time.sleep(random.uniform(0.05, 0.15)) # Use time.sleep for character delay
            page.press(search_box_selector, 'Enter')

            # Wait a moment for the results to load
            page.wait_for_timeout(4000) # Use page.wait_for_timeout for browser-level delay
            
            # 3. Scrape First Hyperlink
            first_link_selector = 'li.b_algo h2 a'
            
            link_element = page.query_selector(first_link_selector)
            
            if link_element:
                # Get the href attribute (the actual URL)
                first_hyperlink = link_element.get_attribute('href')
            else:
                first_hyperlink = "Error: First link element not found on the search results page."

            browser.close()
            
    except Exception as e:
        first_hyperlink = f"Fatal Error: {e}"
        
    return first_hyperlink

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route to handle search queries and return ONLY the first hyperlink.
    """
    search_term = "Default Search"
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            search_term = data.get('search_term')
        except:
            return Response("Error: Invalid JSON or missing 'search_term' in POST request.", status=400, mimetype='text/plain')
    
    elif request.method == 'GET':
        search_term = request.args.get('search_term', 'SouthAfrica VS India')
        
    if not search_term:
        return Response("Error: Search term cannot be empty.", status=400, mimetype='text/plain')
    
    # Run the core Playwright logic synchronously within the Flask route
    result_url = run_playwright_search_sync(search_term)
    
    # Return ONLY the first hyperlink as plain text, as requested
    return Response(result_url, status=200, mimetype='text/plain')

@app.route('/health')
def health_check():
    """Simple health check endpoint."""
    return Response("status: ok", status=200, mimetype='text/plain')

# --- Run the Application ---
if __name__ == "__main__":
    app.run(debug=True)