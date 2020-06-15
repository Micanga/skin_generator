import cv2
import imageio
import imutils
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import re
import sys

# 1. Segmentation
image = sys.argv[1]
#os.system("python3 Fashion-AI-segmentation/run.py "+image)

m = re.search('/(.+?)\.', image)
if m:
	processing_id = m.group(1)
else:
	print('IdError: processing id extraction error.\nNot found in',image,'.') 
	exit(1)

# 2. Pre-processing the output
# a. removing the transparent pixels
image = Image.open("0-"+processing_id+"-out.png")
image.convert("RGBA") # Convert this to RGBA if possible

if image.mode == "RGBA":
	# - loading the pixel data
	pixel_data = image.load()
	for y in range(image.size[1]):
		for x in range(image.size[0]):
			# - if it's opaque, fill white
			if pixel_data[x, y][3] < 0.9*255:
				pixel_data[x, y] = (255, 255, 255, 255)

image.save('1-'+processing_id+'-notransparent.png') 

# b. contouring the the image
img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
edges = cv2.Canny(img, 10, 100)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
dilated = cv2.dilate(edges,kernel,iterations = 1)

cimg, contours, hierarchy = cv2.findContours(dilated.copy(),  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
max_area, max_area_contour = 0, -1
for i,contour in enumerate(contours):
	if hierarchy[0][i][3] == -1:
		area = cv2.contourArea(contour)
		if area > 1000.0:
			if max_area < area:
				max_area = area
				max_area_contour = i
			cv2.drawContours(img, contours, i, (0,255,255), 0)

cv2.imwrite('2-'+processing_id+'-contured.png', img)

# c. removing the area outside of contour
mask = np.zeros(img.shape, np.uint8)
for i in range(len(contours)):
	if i != max_area_contour and hierarchy[0][i][3] == -1:
		cv2.drawContours(mask, contours, i, (255,255,255,255), -1)
removed = cv2.add(img, mask)

cv2.imwrite("3-"+processing_id+"-removed.png", removed)