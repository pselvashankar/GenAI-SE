import pyautogui
import time
import sys
import os 

# --- PRE-REQUISITES & CONFIGURATION ---
# 1. SET YOUR SCREEN RESOLUTION: PyAutoGUI scripts are highly sensitive to screen resolution.
# 2. FILE LOCATION: The script will save the screenshot in the directory from which it is run.
# 3. CALIBRATE COORDINATES FOR PARTIAL SCREENSHOT:
#    The `region` parameters (left, top, width, height) below are ESTIMATED from the sample image.
#    You might need to adjust them for your specific monitor and browser setup.

# Set a delay between all PyAutoGUI actions for stability
pyautogui.PAUSE = 0.5 

print("--- Starting Automation Script (Partial Screenshot Mode) ---")

try:
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

    # --- STEP 2: Perform Search ---
    
    # 4. Type the search query
    search_query = 'weather forecast tomorrow in Chennai'
    print(f"4. Searching for: '{search_query}'...")
    pyautogui.write(search_query)
    pyautogui.press('enter')
    time.sleep(4) # Wait for search results and the weather card to load

    # --- STEP 3: Take Partial Screenshot of Weather Card ---
    
    # Define the region for the screenshot (left, top, width, height)
    # These are ESTIMATED based on your provided image.
    # You may need to adjust these values using pyautogui.displayMousePosition()
    # or by trial and error on your system.
    # For a 1920x1080 screen, these might be a good starting point.
    region_left = 217  # X-coordinate of the left edge of the region
    region_top = 249   # Y-coordinate of the top edge of the region
    region_width = 700 # Width of the region
    region_height = 400 # Height of the region

    # Generate a unique filename using a timestamp
    screenshot_filename = f'chennai_weather_card_{int(time.time())}.png'
    
    # Take the partial screenshot
    print(f"5. Taking partial screenshot of weather card (region: {region_left},{region_top},{region_width},{region_height}) and saving as '{screenshot_filename}'...")
    pyautogui.screenshot(screenshot_filename, region=(region_left, region_top, region_width, region_height))
    time.sleep(1) # Wait for screenshot to be saved

    print("\n--- CAPTURE SUCCESSFUL ---")
    print(f"Partial screenshot saved to the current directory: {screenshot_filename}")
    print("-----------------------------\n")

    # Close the browser 
    # Use Alt+F4 to close the active window
    print("6. Closing Edge browser...")
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1) 
    
    print("--- Script Finished Successfully ---")

except Exception as e:
    print(f"\nAn error occurred during automation: {e}")
    # Use pyautogui fail-safe (close active window) to stop if something goes wrong
    pyautogui.hotkey('alt', 'f4') 
    sys.exit(1)