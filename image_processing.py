import cv2
import imageio
import imutils
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import re

class ImageProcessor:

	def __init__(self,filename):
		self.image_id = self.get_id(filename)
		self.resolutions = {'AnimalCrossing':64}

	def get_id(self,filename):
		m = re.search('/(.+?)\.', filename)
		if m:
			image_id = m.group(1)
			return image_id
		else:
			print('IDError: id match find error.\nPattern not found in',filename,'.') 
			exit(1)

	def prep_run(self):
		# a. removing the transparent pixels
		print('- Removing Transparency')
		self.remove_transparency()

		# b. contouring the image
		print('- Contouring')
		img, contour, hierarchy, max_area_contour = self.contour()

		# c. removing the area outside of contour
		print('- Removing Small Contours')
		self.remove_small_contours(img,contour,hierarchy, max_area_contour)

	def remove_transparency(self):
		image = Image.open("results/1-"+self.image_id+"-seg.png")
		image.convert("RGBA") # Convert this to RGBA if possible

		if image.mode == "RGBA":
			# - loading the pixel data
			pixel_data = image.load()
			for y in range(image.size[1]):
				for x in range(image.size[0]):
					# - if it's opaque, fill white
					if pixel_data[x, y][3] < 0.9*255:
						pixel_data[x, y] = (255, 255, 255, 255)

		image.save('results/2-'+self.image_id+'-notransparent.png') 
		image.close()

	def contour(self):
		image = Image.open("results/2-"+self.image_id+"-notransparent.png")
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

		cv2.imwrite('results/3-'+self.image_id+'-contured.png', img)
		image.close()
		return img, contours, hierarchy, max_area_contour

	def remove_small_contours(self,img,contours,hierarchy, max_area_contour):
		mask = np.zeros(img.shape, np.uint8)
		for i in range(len(contours)):
			if i != max_area_contour and hierarchy[0][i][3] == -1:
				cv2.drawContours(mask, contours, i, (255,255,255,255), -1)
		prep = cv2.add(img, mask)

		cv2.imwrite("results/4-"+self.image_id+"-prep.png", prep)

	def click_and_crop(self,event, x, y, flags, param):
		global refPt
		# if the left mouse button was clicked, record the starting
		# (x, y) coordinates and indicate that cropping is being
		# performed
		if event == cv2.EVENT_LBUTTONDOWN:
			refPt = [(x, y)]
			poly.append([x,y])
		# check to see if the left mouse button was released
		elif event == cv2.EVENT_LBUTTONUP:
			# record the ending (x, y) coordinates and indicate that
			# the cropping operation is finished
			refPt.append((x, y))
			# draw a rectangle around the region of interest
			cv2.line(self.image, refPt[0], refPt[1], (0, 255, 0), 2)
			cv2.imshow("image", self.image)

	def remove_perspective(self):
		img = Image.open("results/4-"+self.image_id+"-prep.png")
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

		# load the image, clone it, and setup the mouse callback function
		clone = img.copy()
		cv2.namedWindow("image")
		cv2.setMouseCallback("image", self.click_and_crop)
		# keep looping until the 'q' key is pressed
		global poly
		poly = []
		while True:
			self.image = img
			# display the image and wait for a keypress
			cv2.imshow("image", img)
			key = cv2.waitKey(1) & 0xFF
			# if the 'r' key is pressed, reset the cropping region
			if key == ord("r"):
				poly = []
				img = clone.copy()
			# if the 'c' key is pressed, break from the loop
			elif key == ord("c"):
				pts1 = np.float32(poly) 
				pts2 = np.float32([[0, 400], [0, 0], [400, 0], [400, 400]]) 
				matrix = cv2.getPerspectiveTransform(pts1, pts2) 
				result = cv2.warpPerspective(clone.copy(), matrix, (400, 400)) 
				cv2.imshow("NoPersp", result)
				cv2.waitKey(0)
			elif key == ord("y"):
				cv2.destroyAllWindows()
				break

		cv2.imwrite("results/5-"+self.image_id+"-nopersp.png", result)

	def cut_n_resize(self):
		print('- Cutting')
		image = Image.open("results/5-"+self.image_id+"-nopersp.png")
		img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
		print('Original Dimensions : ',img.shape)

		width, height = img.shape[0], img.shape[1]

		x_min,x_max,y_min,y_max = 0,0,0,0
		break_flag = False
		for x in range(width):
			for y in range(height):
				if img[x,y,0] != 255 or img[x,y,1] != 255\
				or img[x,y,2] != 255:
					x_min = x
					break_flag = True
					break
			if break_flag:
				break

		break_flag = False
		for x in reversed(range(width)):
			for y in reversed(range(height)):
				if img[x,y,0] != 255 or img[x,y,1] != 255\
				or img[x,y,2] != 255:
					x_max = x
					break_flag = True
					break
			if break_flag:
				break

		break_flag = False
		for y in range(height):
			for x in range(width):
				if img[x,y,0] != 255 or img[x,y,1] != 255\
				or img[x,y,2] != 255:
					y_min = y
					break_flag = True
					break
			if break_flag:
				break

		break_flag = False
		for y in reversed(range(height)):
			for x in reversed(range(width)):
				if img[x,y,0] != 255 or img[x,y,1] != 255\
				or img[x,y,2] != 255:
					y_max = y
					break_flag = True
					break
			if break_flag:
				break

		print(x_min,x_max,y_min,y_max)

		crop_img = img[x_min:x_max, y_min:y_max	]


		print('Cropped Dimensions : ',crop_img.shape)
		print('- Resizing')
		print('Original Dimensions : ',crop_img.shape)

		width = int(self.resolutions["AnimalCrossing"])
		height = int(self.resolutions["AnimalCrossing"])
		dim = (width, height)
		resized = cv2.resize(crop_img, dim, interpolation = cv2.INTER_AREA)

		print('Resized Dimensions : ',resized.shape)
		cv2.imwrite("results/6-"+self.image_id+"-resized.png", resized)