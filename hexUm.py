#!/usr/bin/env python3

import numpy as np
import random
import datetime
import time

hex_vals = []

def remove_leading_zeros(rack):
	''' remove leading zeros '''
	found_non_zero = False
	signifigant_digits = []
	for i in rack:
		if i !=0:
			found_non_zero = True
		if found_non_zero:
			signifigant_digits.append(i)
	return signifigant_digits if signifigant_digits else[0] 

def dec_2_hex(signifigant_digits):
	''' attempt to convert decimal to hexadecimal '''
	rosetta = {
	0: '0',
	1: '1',
	2: '2',
	3: '3',
	4: '4',
	5: '5',
	6: '6',
	7: '7',
	8: '8',
	9: '9',
	10:'A',
	11:'B',
	12:'C',
	13:'D',
	14:'E',
	15:'F'
	}
	
	global hex_vals
	hex_vals = []
	
	for i in signifigant_digits:
		if i in rosetta:
			hex_vals.append(rosetta[i])
		else:
			print(f"check yo self!")
	return hex_vals

def find_hex_value(num):
	''' find decimal value of hexadecimal
	positions ('rack'). '''

	j = num // 68719476736
	remainder = num % 68719476736

	i = remainder // 4294967296
	remainder = remainder % 4294967296

	h = remainder // 268435456
	remainder = remainder % 268435456

	g = remainder // 16777216
	remainder = remainder % 16777216

	f = remainder // 1048576
	remainder = remainder % 1048576

	e = remainder // 65536
	remainder = remainder % 65536

	d = remainder // 4096
	remainder = remainder % 4096

	c = remainder // 256
	remainder = remainder % 256

	b = remainder // 16
	a = remainder % 16
	
	combined_value = j * 68719476736 + i * 4294967296 + h * 268435456 + g * 16777216 + f * 1048576 + e * 65536 + d * 4096 + c * 256 + b * 16 + a * 1
	rack = [j,i,h,g,f,e,d,c,b,a]

	signifigant_digits = remove_leading_zeros(rack)
	hex_as_list = dec_2_hex(signifigant_digits)
	
	print(f"Decimal Representation: {combined_value}")
	print(f"Hexidecimal Representation by 'hex': {hex(num).upper()}")
	hex_as_str = ''.join(map(str,hex_as_list))
	print(f"Hexidecimal Representation by me: {hex_as_str}")

def go_logic():	
	while True:
		try: 
			trigger = int(input("Give me a number:\n"))
			find_hex_value(trigger)
		except ValueError:
			print(f'I said number, fool!')

go_logic()
