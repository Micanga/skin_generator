import cv2
import imageio
import imutils
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

# 1. Segmentation
#print('Input image: ',end='')
#image = str(input())
#os.system("python3 Fashion-AI-segmentation/run.py "+image)

# 2. Pre-processing the output
# a. removing the transparent pixels
image = Image.open("out.png")
image.convert("RGBA") # Convert this to RGBA if possible

if image.mode == "RGBA":
	# - loading the pixel data
	pixel_data = image.load()
	for y in range(image.size[1]):
		for x in range(image.size[0]):
			# - if it's opaque, fill white
			if pixel_data[x, y][3] < 0.9*255:
				pixel_data[x, y] = (255, 255, 255, 255)

image.save('1-notransparent.png') 
image.close()

# b. contouring the the image
img = cv2.imread("1-notransparent.png", 0)
edges = cv2.Canny(img, 10, 100)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
dilated = cv2.dilate(edges,kernel,iterations = 1)

contours = cv2.findContours(dilated.copy(),  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
for i,contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if area > 1000.0:
        cv2.drawContours(img, contours, i, (0,255,255), 2)

cv2.imwrite('2-contured.png', img)

# c. removing the area outside of contour
mask = np.zeros(img.shape, np.uint8)
sorted_areas = sorted(contours, key=cv2.contourArea)
for area in sorted_areas[0:-1]:
	cv2.drawContours(mask, [area], 0, (255,255,255,255), -1)
removed = cv2.add(img, mask)

cv2.imwrite("3-removed.png", removed)