import random
import threading
import time

import cv2
import keyboard
import numpy as np
import pytesseract

try:
	import Image
except ImportError:
	from PIL import Image, ImageGrab

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def processImage():
	readImage = cv2.imread('screenshot.png')
	imageHeight, imageWidth = readImage.shape[:2]

	lowerWidthBound = int(.29 * imageWidth)  # 555px / 1920px
	upperWidthBound = int(.375 * imageWidth)  # 720px / 1920px
	lowerHeightBound = int(.435 * imageHeight)  # 615px / 1080px
	upperHeightBound = int(.57 * imageHeight)  # 470px / 1080px

	# Crop and block out colors on the image
	croppedImage = readImage[lowerHeightBound:upperHeightBound, lowerWidthBound:upperWidthBound]

	lowerColorBound = np.array([27, 27, 27], dtype="uint16")
	upperColorBound = np.array([50, 50, 50], dtype="uint16")
	colorMask = cv2.inRange(croppedImage, lowerColorBound, upperColorBound)

	# Find text contours
	imageContours, imageHierarchy = cv2.findContours(colorMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# Create lists to hold our Tesseract data
	possibleChars = []
	possibleCharsData = []

	# Process everything that may be text
	for possibleText in imageContours:
		# Create a bounding rectangle around the contour
		[x, y, width, height] = cv2.boundingRect(possibleText)

		# Draw rectangles around the contours on the original image
		cv2.rectangle(colorMask, (x, y), (x + width, y + height), (255, 0, 255), 0)
		# Create our region of interest
		regionOfInterest = colorMask[y: (y + height), x: (x + width)]

		# Enlarge the region
		enlargedImage = cv2.copyMakeBorder(regionOfInterest, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])

		# Run Tesseract OCT against the image to try and find the most likely keystroke
		possibleChars.append(pytesseract.image_to_string(regionOfInterest, lang='eng',
		                                                 config='--psm 10 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz'))
		possibleCharsData.append(pytesseract.image_to_data(regionOfInterest, lang='eng',
		                                                   config='--psm 10 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz'))

	# Return all of the possible characters for the AFK key
	return possibleChars, possibleCharsData


def findMaxConfidence(possibleChars, possibleCharData):
	confidenceValues = {}

	# Process the character data and find the highest confidence
	for possibleChar in possibleCharData:

		newlinedData = possibleChar.split('\n')

		for charLevel in newlinedData:
			formattedData = charLevel.split('\t')

		# If there exists a confidence and the text is one letter add it to the possible values
		if int(formattedData[10]) > -1 and len(formattedData[11]) == 1:
			# Add the letter as the key, and the confidence as the value
			confidenceValues[formattedData[11]] = formattedData[10]

	# Find the most likely character and its confidence
	if len(confidenceValues) > 0:
		maxConfidence = max(confidenceValues.values())
		confidenceCharacter = list(confidenceValues.keys())[list(confidenceValues.values()).index(maxConfidence)]

		return maxConfidence, confidenceCharacter
	# If we couldn't determine a character, return a dash
	else:
		return 0, "-"


def screenshotLoop():
	# Take a screenshot so that we can check for the AFK check
	print("[Anti-AFK] Taking a screenshot")
	screenshotImage = ImageGrab.grab()
	screenshotImage.save('screenshot.png')

	# Create a list of all possible characters for the AFK key
	possibleChars, possibleCharsData = processImage()
	print("[Anti-AFK] Found possible characters: " + "[%s]" % ", ".join(map(str, possibleChars)))

	# Find the most likely character using confidence
	highestConfidence, confidenceCharacter = findMaxConfidence(possibleChars, possibleCharsData)

	print("[Anti-AFK] Most confident in character: " + confidenceCharacter + " (with confidence of " + str(
		highestConfidence) + ")")

	if confidenceCharacter is not "-":
		print("[Anti-AFK] Pressing character \"" + str(confidenceCharacter) + "\"")
		keyboard.press_and_release(confidenceCharacter)
	else:
		print("[Anti-AFK] ERROR: No confidence character found. Please manually input a character")

	print("[Anti-AFK] Sleeping for 15 minutes")
	threading.Timer(float(900), spinLoop).start()


def spinLoop():
	# Press spacebar to simulate a slot machine pull
	keyboard.press_and_release('space')

	print("[Spin] Slot machine pulled...", end=' ')

	# Wait 5 to 15 seconds
	sleepTime = random.randint(5, 15)
	threading.Timer(float(sleepTime), spinLoop).start()

	print("Sleeping for " + str(sleepTime) + " seconds")


if __name__ == "__main__":
	print("[Main] Program starting in 5 seconds...", end=' ')
	time.sleep(5)
	print("Starting!")

	spinLoop()
	screenshotLoop()
