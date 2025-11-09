import pyautogui
import time
import os
"""
#Mouse Operations
# Move the mouse to a specific position
#pyautogui.moveTo(100, 100, duration=1)
#time.sleep(1)  
# Click at the current position
#pautogui.click()
    
# Double click
#pyautogui.doubleClick()
    
 # Right click
pyautogui.rightClick()
    
# Drag the mouse to a new position
#pyautogui.dragTo(200, 200, duration=1)

time.sleep(4)

pyautogui.click(1807,769,duration=3)
pysutogui.doubleClick(1807,769,duration=3)
pyautogui.rightClick(1807,769,duration=3)   
pyautogui.dragTo(200, 200, duration=1)
pyautogui.moveTo(100, 100, duration=1)
pyautogui.scrollUp(500)
pyautogui.scrollDown(500)

#keyboard Operations
#pyautogui.click(573,613,duration=3)
#pyautogui.write("Hello, World!", interval=0.1)

#pyautogui.press("enter")
#pyautogui.write("python RPA_Demo_1.py", interval=0.1)
#pyautogui.press("enter")
#time.sleep(4)
pyautogui.click(1807,769,duration=3)
pyautogui.hotkey("ctrl","a")
# Find the current position of the mouse pointer
#image
location=pyautogui.locateOnScreen("Notification.jpg",confidence=0.9)
print(location)
time.sleep(2)
#pyautogui.click(pyautogui.center(location))
print(pyautogui.size())

ScreenPrint=pyautogui.screenshot()
ScreenPrint.save(os.path.join("E:\\AI-Learning\\GenAI-SE\\pyAutoGUI","screenshot.png"))
"""