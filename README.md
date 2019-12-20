# SlotBot
A bot written in Python 3.7 that allows users to automate the playing of slot machines on the game Tower Unite. Please read all of the contents below before running this script. **I will not be providing support for this script.**

## Authors Note (Disclaimer)
**Using automated scripts such as this can get you banned from Tower Unite. Tower Unite uses Valve Anti-Cheat (VAC) and you will be restricted from all online play PERMANENTLY on games which use VAC should you get banned. Please use this at your own risk and don't hold me liable if you get banned. I had originally not intend to publish this script, but figured it would be a waste of hard work and time not to publish it. It's also very likely that by the time you are reading this, Tower Unite has worked around such methods to bypass their Anti-AFK checking on the slot machines.**

You can read more about Valve Anti-Cheat here: https://support.steampowered.com/kb/7849-RADZ-6869/


## Features
* Automatically plays the Tower Unite slot machines by pressing the spacebar at random intervals
* Checks for an "Anti-AFK Check" every 15 minutes
* Performs Optical Character Recognition (OCR) using Tesseract and OpenCV2 to find which "Anti-AFK" key to press
* Creates a confidence for each possible keypress
* Presses the most likely "Anti-AFK" key

## Requirements
* Python v3.7
* Tesseract OCR
* Python Libraries:
  * keyboard
  * numpy
  * opencv-python
  * pandas
  * pyscreenshot
  * pytesseract
  * PIL, Image, ImageGrab (refer to script imports)
  
 ## Setup
 1. Download the script
 2. Install all requirements listed above
 3. Edit [Line 15](https://github.com/Bonfire/SlotBot/blob/8f29ff97510e4471d1a9c84decd2adf3e343608c/SlotBot.py#L15) in `SlotBot.py` and input the location of where you installed `tesseract.exe` from Tesseract OCR
 4. Edit the lower and upper height and width bounds on [Lines 22 through 25](https://github.com/Bonfire/SlotBot/blob/8f29ff97510e4471d1a9c84decd2adf3e343608c/SlotBot.py#L22) to match where the "Anti-AFK Check" would be on your screen. This may take some time to figure out exactly where it would appear depending on your screen size and resolution.
 5. Run the script!

## Use
You should use the slot machine until you are presented with an AFK check. Once you get an AFK check, you should run the script as it'll make it so that the script and the check are on the same schedule of 15 minutes.

This script will send a spacebar keyboard input every 5 to 15 seconds. This script will also attempt to take a screenshot of the window in the foreground on your computer every 15 minutes for OCR processeing. As a result, it's required that you are not actually doing anything else while running the script. This script was intended for overnight use.
