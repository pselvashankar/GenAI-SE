import pyautogui
import time
import sys

# --- Configuration ---
# Set a short pause after every pyautogui function call for stability
pyautogui.PAUSE = 0.5 

# Target contact and message
CONTACT_NAME = "Selva"
# Define the message to be sent as requested
AUTOMATED_MESSAGE = "Test"

def open_whatsapp_and_send_message():
    """
    Automates opening WhatsApp, searching for a contact, opening the chat, 
    and sending the specified message using a double-click heuristic and 
    image recognition for the message input box.
    
    NOTE: This script requires a screenshot of the message input box 
    named 'type_a_message.png' in the same directory.
    """
    print("Step 1: Launching WhatsApp application...")
    
    try:
        # 1. Launch WhatsApp using the Windows Start Menu search
        pyautogui.press('win') 
        time.sleep(1) # Give time for the start menu to appear
        
        pyautogui.write('whatsapp')
        pyautogui.press('enter')
        
        # Increased wait time for robust startup
        time.sleep(7) 
        
        # 2. Search for the contact
        print(f"Step 2: Searching for contact '{CONTACT_NAME}'...")
        
        # Ensure the search bar is focused (Ctrl+F is the common shortcut)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        
        pyautogui.write(CONTACT_NAME)
        time.sleep(2) # Wait for search results to filter
        
        # FIX A (Select Contact): Using double-click at an estimated screen coordinate
        ESTIMATED_X = 250
        ESTIMATED_Y = 200
        print(f"Attempting to double-click the contact at estimated screen position ({ESTIMATED_X}, {ESTIMATED_Y})...")
        
        pyautogui.moveTo(ESTIMATED_X, ESTIMATED_Y, duration=0.25)
        pyautogui.doubleClick() 
        time.sleep(3) # Wait for the chat to fully load

        # 3. Focus Message Box using Image Recognition (The requested fix)
        MESSAGE_INPUT_IMAGE = "type_a_message.png"
        print(f"Step 3: Finding and clicking the 'Type a message' box using '{MESSAGE_INPUT_IMAGE}'...")
        
        # Use locateOnScreen to find the exact location of the message box element
        input_location = pyautogui.locateOnScreen(MESSAGE_INPUT_IMAGE, confidence=0.8)
        
        if input_location:
            # Click the center of the located area
            pyautogui.click(input_location) 
            time.sleep(1)
            print("Successfully clicked the message input box.")
        else:
            print(f"ERROR: Could not find '{MESSAGE_INPUT_IMAGE}' on screen. Please ensure the file exists and is visible.")
            # If image recognition fails, exit gracefully (or you can add a fallback).
            return 

        # 4. Write and Send the Message
        print(f"Step 4: Sending message: '{AUTOMATED_MESSAGE}'")
        pyautogui.write(AUTOMATED_MESSAGE)
        time.sleep(1) # Wait slightly before sending
        pyautogui.press('enter') # Press Enter to send the message

        print(f"\n--- Automation Complete ---")
        print(f"Message '{AUTOMATED_MESSAGE}' successfully sent to contact: {CONTACT_NAME}.")
        
    except Exception as e:
        print(f"An error occurred during automation: {e}")
        print("Please ensure your screen is visible and WhatsApp is installed and accessible.")


if __name__ == "__main__":
    try:
        # Simple check for running in a potentially restrictive environment
        if 'sys.stdin.isatty' in dir(sys.stdin) and not sys.stdin.isatty():
             print("WARNING: This script performs actions on your physical screen (mouse/keyboard). Run it carefully.")
        
        open_whatsapp_and_send_message()
        
    except Exception as e:
        print(f"A critical error occurred: {e}")