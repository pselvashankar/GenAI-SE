import pyautogui
import time
import sys
import os
import pyperclip # NEW: We need this library to get content from the clipboard

# --- PRE-REQUISITES & CONFIGURATION ---
# NOTE: You need to install the pyperclip library: pip install pyperclip
# 1. SET YOUR SCREEN RESOLUTION: PyAutoGUI scripts are highly sensitive to screen resolution.
# 2. FILE LOCATION: The script will save the screenshot and HTML file in the run directory.
# 3. CALIBRATE COORDINATES FOR PARTIAL SCREENSHOT: Adjust as needed for your setup.

# Set a delay between all PyAutoGUI actions for stability
pyautogui.PAUSE = 0.5

print("--- Starting Automation Script (Screenshot & HTML Capture) ---")

try:
    # --- STEP 1: Browser Setup and Navigation (Unchanged) ---
    # 1. Open the Start Menu/Search Bar (assuming Windows)
    print("1. Opening Start Menu and searching for Edge...")
    pyautogui.press('win')
    time.sleep(1)

    # 2. Type "edge" and hit Enter
    pyautogui.write('edge')
    time.sleep(1)
    pyautogui.press('enter')

    # Wait for the browser to fully open and load
    print("2. Waiting for Edge to launch...")
    time.sleep(4)

    # 3. Type Google URL in the address bar and navigate
    print("3. Navigating to google.com...")
    # Ensure focus is on the address bar
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.write('www.google.com')
    pyautogui.press('enter')
    time.sleep(3)

    # --- STEP 2: Perform Search (Unchanged) ---
    # 4. Type the search query
    search_query = 'weather forecast tomorrow in Chennai'
    print(f"4. Searching for: '{search_query}'...")
    pyautogui.write(search_query)
    pyautogui.press('enter')
    time.sleep(4) # Wait for search results and the weather card to load

    # --- STEP 3: Take Partial Screenshot of Weather Card (Unchanged) ---
    # Define the region for the screenshot (left, top, width, height)
    region_left = 217
    region_top = 249
    region_width = 700
    region_height = 400

    # Generate a unique filename using a timestamp
    timestamp = int(time.time())
    screenshot_filename = f'chennai_weather_card_{timestamp}.png'

    # Take the partial screenshot
    print(f"5. Taking partial screenshot of weather card and saving as '{screenshot_filename}'...")
    pyautogui.screenshot(screenshot_filename, region=(region_left, region_top, region_width, region_height))
    time.sleep(1) # Wait for screenshot to be saved

    # --- NEW STEP: Get Source Page HTML ---
    html_filename = f'chennai_weather_source_{timestamp}.txt'
    print(f"6. Getting page source HTML and saving to '{html_filename}'...")

    # Press Ctrl+U to open the page source in a new tab/window
    pyautogui.hotkey('ctrl', 'u')
    time.sleep(3) # Wait for the source page to load

    # Select All (Ctrl+A)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)

    # Copy (Ctrl+C)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)

    # Close the source tab (Ctrl+W)
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1) # Wait for the tab to close and focus to return to the search result

    # Get the HTML content from the clipboard
    page_source_html = pyperclip.paste()

    # Write the content to a .txt file
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(page_source_html)

    print("\n--- CAPTURE SUCCESSFUL ---")
    print(f"Partial screenshot saved: {screenshot_filename}")
    print(f"Page source HTML saved: {html_filename}")
    print("-----------------------------\n")

    # --- STEP 5: Close Browser (Unchanged) ---
    # Use Alt+F4 to close the active window (the main Edge browser)
    print("7. Closing Edge browser...")
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)

    print("--- Script Finished Successfully ---")

except Exception as e:
    print(f"\nAn error occurred during automation: {e}")
    # Use pyautogui fail-safe (close active window) to stop if something goes wrong
    pyautogui.hotkey('alt', 'f4')
    sys.exit(1)