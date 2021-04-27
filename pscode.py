from PIL import Image, ImageDraw
import math
import os
from time import sleep


# Variables
WHITE = (255,255,255)
BLACK = (0,0,0)

# FUNCTIONS
def intToBit(integer):
	return format(int(integer), '08b')

def bitToInt(integer):
	value = 0
	for i in range(0, len(integer)):
		if int(integer[i]) == 1 and i == 0:
			value += 128
		elif int(integer[i]) == 1 and i == 1:
			value += 64
		elif int(integer[i]) == 1 and i == 2:
			value += 32
		elif int(integer[i]) == 1 and i == 3:
			value += 16
		elif int(integer[i]) == 1 and i == 4:
			value += 8
		elif int(integer[i]) == 1 and i == 5:
			value += 4
		elif int(integer[i]) == 1 and i == 6:
			value += 2
		elif int(integer[i]) == 1 and i == 7:
			value += 1

	return value

def drawBit(bit, x, y):
	#print(bit)
	row = 0
	for i in range(0,8):
		if bit[i] == "1":
			if i % 2 == 0:
				#left
				draw.point((x, y + row), fill=BLACK)
			else:
				#right
				draw.point((x+1, y + row), fill=BLACK)
				row += 1
		elif i % 2 != 0:
			row += 1

def readBit(image, x, y):
	px = image.load()
	row = 0
	bit =""
	for i in range(0,8):
		if i % 2 == 0:
				#left
				if px[x, y + row] == (0,0,0):
					bit = bit + "1"
				elif px[x, y + row] == (255,255,255):
					bit = bit + "0"
				else:
					print("ERROR\nImage is not an PSCode.")
		else:
				#right
				if px[x+1, y + row] == (0,0,0):
					bit = bit + "1"
					row += 1
				elif px[x+1, y + row] == (255,255,255):
					bit = bit + "0"
					row += 1
				else:
					print("ERROR\nImage is not an PSCode.")
	return bit

def readLenBit(img):
	lenBit = readBit(img, 18,17)
	return bitToInt(lenBit)

def drawBits(rowCount, ASCIIbit):
	for row in range(0, rowCount):
		for col in range(0, 10):
			if len(ASCIIbit) == 1:
				# Checks if bit is last in list: draws and ends the drawing.
				drawBit(ASCIIbit[0], col * 2, row * 4 + 5)
				#print(f"drawing {ASCIIbit[0]} in row {row} and in col {col}")
				return
			else:
				# Draws first bit of list and deletes after
				drawBit(ASCIIbit[0], col * 2, row * 4 + 5)
				#print(f"drawing {ASCIIbit[0]} in row {row} and in col {col}")
				ASCIIbit.pop(0) 

def drawTemplate():
	# Makes the img
	global draw, img
	img = Image.new('RGB', (21, 21), color = 'white') # PSCode is 21x21 big.
	draw = ImageDraw.Draw(img)
	# ROW 0
	draw.rectangle([0,0,2,0], fill=BLACK)
	draw.rectangle([4,0,6,0], fill=BLACK)
	draw.rectangle([8,0,9,0], fill=BLACK)
	draw.rectangle([11,0,13,0], fill=BLACK)
	draw.rectangle([15,0,16,0], fill=BLACK)
	draw.rectangle([19,0,20,0], fill=BLACK)

	# ROW 1
	draw.point((0, 1), fill=BLACK)
	draw.point((2, 1), fill=BLACK)
	draw.point((4, 1), fill=BLACK)
	draw.point((8, 1), fill=BLACK)
	draw.point((11, 1), fill=BLACK)
	draw.point((13, 1), fill=BLACK)
	draw.point((15, 1), fill=BLACK)
	draw.point((17, 1), fill=BLACK)
	draw.point((19, 1), fill=BLACK)

	# ROW 2
	draw.rectangle([0,2,2,2], fill=BLACK)
	draw.rectangle([4,2,6,2], fill=BLACK)
	draw.point((8, 2), fill=BLACK)
	draw.point((11, 2), fill=BLACK)
	draw.point((13, 2), fill=BLACK)
	draw.point((15, 2), fill=BLACK)
	draw.point((17, 2), fill=BLACK)
	draw.rectangle([19,2,20,2], fill=BLACK)

	# ROW 3 
	draw.point((0, 3), fill=BLACK)
	draw.point((6, 3), fill=BLACK)
	draw.point((8, 3), fill=BLACK)
	draw.point((11, 3), fill=BLACK)
	draw.point((13, 3), fill=BLACK)
	draw.point((15, 3), fill=BLACK)
	draw.point((17, 3), fill=BLACK)
	draw.point((19, 3), fill=BLACK)

	# ROW 4
	draw.point((0, 4), fill=BLACK)
	draw.rectangle([4,4,6,4], fill=BLACK)
	draw.rectangle([8,4,9,4], fill=BLACK)
	draw.rectangle([11,4,13,4], fill=BLACK)
	draw.rectangle([15,4,16,4], fill=BLACK)
	draw.rectangle([19,4,20,4], fill=BLACK)

	# COLUMN 20 (dotted)
	for i in range(6, 21):
		if i % 2 == 0:
			draw.point((20, i), fill=BLACK)

def drawLenBit(string):
	# Draws the lenght of the string as an 8bit int in the bottom-right cornor
	bit = intToBit(len(string))
	drawBit(bit, 18, 17)

def stringToASCIIlist(string):
	# Converts the strings characters into ASCII index numbers and stores them in a list.
	ASCII = []
	for i in range(0, len(string)):
		ASCII.append(str(ord(string[i])))
	return ASCII

def saveImg(title):
	img.save(f'{title}.png')
	Image.open("test.png").show()
	print(f"Generated PSCode!\nSaved as /{title}.png")

def makeBitList(ASCII):
	# Converts ASCII index list into 8-bit int and stores them in ASCIIbit[].
	ASCIIbit = []
	# Converting ints to base bit
	for i in ASCII:
		i = intToBit(i)
		ASCIIbit.append(i)

	return ASCIIbit

def calcRows(listOrInt):
	# Calculating the rows for when to draw bits or read bits
	# When reading it will take an int as arg, for drawing a list.
	if type(listOrInt) == list:
		return math.ceil((len(listOrInt) / 10))
	elif type(listOrInt) == int:
		return math.ceil(listOrInt / 10)
	else:
		print("Invalid argument. Must be an int or list.")

def makePSCode(string, title):
	if len(string) > 39:
		print("Text is too long. PSCode only supports up to 40 characters of length.")
		return
	drawTemplate() # Draws PSCode template
	ASCII = stringToASCIIlist(string) # Converts string into ASCII index for each letter => ASCII[]
	ASCIIbit = makeBitList(ASCII) # Converts ASCII[] into 8bit => ASCIIbit[]
	rowsCount = calcRows(ASCIIbit) # Calculates the rows needed to draw the data
	drawLenBit(string)
	drawBits(rowsCount, ASCIIbit) # Draws the actual bits on the PSCode.
	saveImg(title) # Saves the PSCode as /<title>.png


def readPSCode(imgPath):
	try:
		img = Image.open(imgPath) # Opens the image
	except FileNotFoundError:
		print("\nFile does not exist.")
		sleep(1)
		terminalMenu()
	bitLen = readLenBit(img) # Reads the bit on BR cornor. Value is how many bits are on the PSCode
	rowsCount = calcRows(bitLen) # Calculates the rows needed to draw the data on the PSCode
	data = ""
	for row in range(0, rowsCount):
		for col in range(0, 10):
			if bitLen == 1:
				bit = readBit(img ,col * 2, row * 4 + 5)
				data = data + chr(bitToInt(bit))
				return data
			else:
				bit = readBit(img ,col * 2, row * 4 + 5)
				data = data + chr(bitToInt(bit))
				bitLen -= 1


def terminalMenu():
	uInp = ""
	os.system('clear')
	print(''' 

	██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ███████╗
	██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
	██████╔╝███████╗██║     ██║   ██║██║  ██║█████╗  
	██╔═══╝ ╚════██║██║     ██║   ██║██║  ██║██╔══╝  
	██║     ███████║╚██████╗╚██████╔╝██████╔╝███████╗
	╚═╝     ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
	                                                 
		Developed by Pepijn Siddiki
		https://github.com/Pepijn2004/PSCode
	——————————————————————————————————————————————————

		CHOOSE AN OPTION:

	1) Generate PSCode.
	2) Read PSCode.
	3) Quit

		''')

	uInp = input(">> ")

	if uInp == "1":
		print("\n	——————————————————————————————————————————————————\n")
		string = input("PSCode data (max 40): ")
		output = input("Name: ")
		makePSCode(string, output)
		print("\n	——————————————————————————————————————————————————\n")
		print(f"PSCode generated as /{output}.png")
		sleep(2)
		terminalMenu()
	elif uInp == "2":
		print("\n	——————————————————————————————————————————————————\n")
		string = input("PSCode path (/pscode.png): ")
		data = readPSCode(string)
		print(f'\n\nPSCODE Text: "{data}"')
		input("\n\nPress enter to return to the menu.")
		terminalMenu()
		
	elif uInp == "3":
		os.system("clear")
		print('''
	 ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗
	██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝
	██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗  
	██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝  
	╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗
	 ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝
				''')
		sleep(1)
		system('clear')
		quit()
	else:
		print("That's not an option")
		sleep(2)
		terminalMenu()



if __name__ == '__main__':
	try:
		terminalMenu()
		#myPSCode = makePSCode("allehoppa", "test")
		#data = readPSCode("test.png")
		#print(data)
	except:
		os.system('clear')
		print('''
	 ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗
	██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝
	██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗  
	██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝  
	╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗
	 ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝
			''')
		sleep(2)
		os.system('clear')
		quit()


