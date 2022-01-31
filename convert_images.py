# https://pythonexamples.org/python-opencv-convert-image-to-black-and-white/

import cv2

def convertImageToBW(pathToImage):
	print(pathToImage)
	originalImage = cv2.imread(pathToImage)
	grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
	threshold = 150 # 128 is the middle between black and white, so higher number may preserve more details
	finalImage = cv2.threshold(grayImage, 150, 255, cv2.THRESH_BINARY)[1] # binary image
	if pathToImage.endswith(".jpg"):
		cv2.imwrite(pathToImage.replace(".jpg", "_BW.png"), finalImage)
	elif pathToImage.endswith(".png"):
		cv2.imwrite(pathToImage.replace(".png", "_BW.png"), finalImage) 


import os
folder = "./1280CumarIbnSayyid/separators/"
#folder = "./1280CumarIbnSayyid/figures/"
files = os.listdir(folder)
for f in files:
	if not "_BW." in f:
		if f.endswith(".jpg"):
			path = os.path.join(folder, f)
			convertImageToBW(path)
		elif f.endswith(".png"):
			path = os.path.join(folder, f)
			convertImageToBW(path)


