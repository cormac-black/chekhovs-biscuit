#!/usr/bin/env python3

import os
import sys
import cv2
import random
import subprocess
import time
import numpy as np
from picamera2 import Picamera2
from datetime import datetime

camera = Picamera2()
camera.start()

TAKE_PHOTO = True
PHOTOS_DIR = '/home/pi1/new_photos'
CARTOON_DIR = '/home/pi1/photos_cartoon'
USB_DRIVE_PATH = "/home/pi1/photo2"

def capture(name):
	'''creates countdown, defines file path and captures initial image'''
	for i in range(5, 0, -1):
		print(i)
		time.sleep(.2)
	file_path = f'{PHOTOS_DIR}/{name}_{datetime.now():%H-%M-%S}.jpg'
	camera.capture_file(file_path)
	print('Photo Taken! \n')
	return file_path

def show_image(file_path):
	'''shows image to defined area of screen using 'feh' and 'os' '''
	geometry = "640x480+1200+250"
	try:
		subprocess.run(['feh', '--no-fehbg', '--geometry', geometry, file_path])
	except subprocess.CalledProcessError as e:
		print(f"Failed to open image with feh: {e}")


def get_image_path(take_photo): 
	''' checks global 'TAKE_PHOTO' (default=True) as boolean,False>USB,True>'capture'
        collects user {name} to pass to 'capture' '''
	if not take_photo:  # False
		if not os.path.exists(USB_DRIVE_PATH):
			print(f"Error: USB drive path {USB_DRIVE_PATH} does not exist!")
			sys.exit(1)
		image_files = [f for f in os.listdir(USB_DRIVE_PATH) if f.lower().endswith(('.jpg', '.png'))]
		image_file = random.choice(image_files)
		image_path = os.path.join(USB_DRIVE_PATH, image_file)
	else:               # True
		print(' ')
		name = input("Enter your name: ")
		input("Press Enter to Take Photo")
		image_path = capture(name)
	return image_path
	

def posterize_it(img):
	'''cartoonizes image'''
	gray = img.copy()
	gray = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
	edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
								  cv2.THRESH_BINARY, 9, 5)
	pixel_values = img.reshape((-1,3))
	pixel_values = np.float32(pixel_values)
	k = 8
	_, labels, centers = cv2.kmeans(pixel_values, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2), 10, cv2.KMEANS_RANDOM_CENTERS)
	
	centers = np.uint8(centers)
	quantized_img = centers[labels.flatten()]
	quantized_img = quantized_img.reshape(img.shape)
	return quantized_img

def apply_colormap(img, gray_img):
	'''applies random color_map or gradient to grayscaled image
    displays random key and value:color_map name to command line
    converts grayscaled image back to BGR '''

	colormap_dict = {
	0: "cv2.COLORMAP_AUTUMN",
	1: "cv2.COLORMAP_BONE", ##
	2: "cv2.COLORMAP_JET",
	3: "cv2.COLORMAP_WINTER", #* 
	4: "cv2.COLORMAP_RAINBOW",
	5: "cv2.COLORMAP_OCEAN",
	6: "cv2.COLORMAP_SUMMER",
	7: "cv2.COLORMAP_SPRING",
	8: "cv2.COLORMAP_COOL",
	9: "cv2.COLORMAP_HSV",
	10: "cv2.COLORMAP_PINK", ##
	11: "cv2.COLORMAP_HOT",
	12: "cv2.COLORMAP_PARULA",
	13: "cv2.COLORMAP_MAGMA",
	14: "cv2.COLORMAP_INFERNO",
	15: "cv2.COLORMAP_PLASMA",
	16: "cv2.COLORMAP_VIRIDIS",
	17: "cv2.COLORMAP_CIVIDIS",
	18: "cv2.COLORMAP_TWILIGHT",
	19: "cv2.COLORMAP_TWILIGHT_SHIFTED",
	20: "cv2.COLORMAP_TURBO",
	21: "cv2.COLORMAP_DEEPGREEN"
	}
    
	alpha = 0.7 # weight of original image
	beta = 0.3  # weight of colormapped image      
	gamma = 0.5 # adjustment to final result, usu. normalized to 1  
    
	print('Your colormap options are: ')
	for i in range(0,21):
		if i == 19:
			print("19 TWILIGHT SHIFTED") # two terms, special case
		else:
			print(i, colormap_dict[i].split('_')[-1]) # remove item before split
	answer = int(input("Please choose a NUMBER: "))
	print('You chose: ', answer,'->', colormap_dict[answer],'\n')

	color_mapped_img = cv2.applyColorMap(gray_img, answer)
	if len(img.shape) == 2 or img.shape[2] == 1:
		img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)    
	blended_img = cv2.addWeighted(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), alpha, color_mapped_img, beta, gamma)
	#blended_img = cv2.addWeighted(img, alpha, color_mapped_img, beta, gamma)

	return blended_img

def find_edges(img, gray):
	''' finds edges (pixels with a threshold level difference) and masks them''' 
	# cv2.Canny() checks adjacent pixel values 
	edges = cv2.Canny(gray, 50, 165)  # << sensitivity of edge-finding, 0-255
	kernel = np.ones((1,1), np.uint8) # << size of edge line
	dilated_edges = cv2.dilate(edges, kernel, iterations=1)

	# Make a copy of the original image to not alter it directly
	result = img.copy()

	# Set the edge pixels to black
	result[dilated_edges != 0] = [0, 0, 0]
	return result
    
def overlay(original, posterized):
	'''returns an image that combines the posterized and original image'''
	overlayed = cv2.addWeighted(original, 0.5, posterized, 0.5, 0) #<< weights of each image
	return overlayed

def print_image(image_path):
	print_command = (f'lp {image_path}')
	os.system(print_command)

def process_image(img):
	'''calls image processing functions and accesses returned values '''
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img1 = posterize_it(img)
	img2 = find_edges(img1, gray)
	img3 = apply_colormap(img2, gray)
	overlayed = overlay(img, img3)
	return img3, overlayed

def main():
	''' drives logic of the program '''
	retake = True
	while retake:
		image_path = get_image_path(TAKE_PHOTO) # 1st call 
		img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
		if img is not None and img.shape[2] == 4:
			img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

		posterized, overlayed = process_image(img)

		new_img_path = image_path.replace(PHOTOS_DIR, CARTOON_DIR).replace('.jpg', '_cart.jpg')
		overlay_path = image_path.replace(PHOTOS_DIR, CARTOON_DIR).replace('.jpg', '_overlay.jpg')
		os.makedirs(os.path.dirname(new_img_path), exist_ok=True)
		os.makedirs(os.path.dirname(overlay_path), exist_ok=True)
		print('Displaying posterized image then overlayed image')
		cv2.imwrite(new_img_path, posterized)
		cv2.imwrite(overlay_path, overlayed)

		show_image(new_img_path)
		show_image(overlay_path)

		time.sleep(0.5)
		cv2.destroyAllWindows()

		answer = input("Do you want to retake? ('y' or 'n'): ")
		retake = answer.lower() == 'y'  # if retake were False at top 
										# this line would re-enforce that
										# '==' is the boolean
	#print image
	print(' ')
	print("Would you like to print?")
	print("1 - print posterized image")
	print("2 - print overlayed image")
	print("0 - no thanks!")
	ans = input("Please choose a NUMBER: ")
	if ans == '1':
		print_image(new_img_path)
	elif ans == '2':
		print_image(overlay_path)

	print("Thank you for visiting!!")


	camera.close()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
