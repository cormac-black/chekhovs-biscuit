#!/usr/bin/env python3

import os
import sys
import cv2
import numpy as np
import random
import subprocess


usb_path = "/media/primo/TWOGIGS/wdw/"

def get_images(path):
	'''searches path folder for valid extensions and returns file''' 
	valid_ext = ('.jpg','.jpeg', '.png' )
	files = [os.path.join(usb_path,f) for f in os.listdir(usb_path) if f.lower().endswith(valid_ext)]
	return files

def picker(files):
	'''chooses image at random and returns the file path''' 
	image_file = random.choice(files)
	image_path = os.path.join(usb_path, image_file)	
	return image_path

def resize(img):
	[hgt,wdth] = img.shape[:2]
	image_aspect_ratio = wdth/hgt

	if 640/480 > image_aspect_ratio:
		new_width = int(hgt * image_aspect_ratio)
		new_height = hgt
	else:
		new_width = wdth
		new_height = int(wdth / image_aspect_ratio) 
	resized_image = cv2.resize(img, (new_width, new_height))
	return resized_image

def show_image(path):
	obj = cv2.imread(path,cv2.IMREAD_UNCHANGED)
	img = resize(obj)
	try:
		geometry = "960x640+1000+200"
		subprocess.run(['feh', '--no-fehbg','--geometry',geometry, path])
	except subprocess.CalledProcessError as e:
		print(f"Failed to open image with feh: {e}")


files = get_images(usb_path)
path = picker(files)
show_image(path)

cv2.waitKey()
cv2.destroyAllWindows()
