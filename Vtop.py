import sys
import time
# sys.path.append('c:/users/jatin dhall/anaconda3/lib/site-packages')
import selenium
from selenium import webdriver
import cv2
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
import os
import json

driver = webdriver.Chrome(ChromeDriverManager().install())

def find(op,text):
	flag = 0
	if op == 1: #Search by id
		while(flag == 0):
			try:
				element = driver.find_element_by_id(text)
				flag = 1
				return element
			except:
				time.sleep(1)
	elif op == 2: #Search by link text
		while(flag == 0):
			try:
				element = driver.find_element_by_link_text(text)
				flag = 1
				return element
			except:
				time.sleep(1)
	elif op == 3: #Search by xpath
		while(flag == 0):
			try:
				element = driver.find_element_by_xpath(text)
				flag = 1
				return element
			except:
				time.sleep(1)
	elif op == 4: #Using css selector
		while(flag == 0):
			try:
				element = driver.find_element_by_css_selector(text)
				flag = 1
				return element
			except:
				time.sleep(1)
	elif op == 5: #Using name
		while(flag == 0):
			try:
				element = driver.find_element_by_name(text)
				flag = 1
				return element
			except:
				time.sleep(1)

def DAUpload():
	
	acadBtn = find(2,"Academics")
	acadBtn.click()
	# driver.find_element_by_link_text("Academics").click()

	# identifying the link with the help of link text locator
	Dabtn = find(1,"EXM0017")
	# button = driver.find_element_by_id("EXM0017")
	driver.execute_script("arguments[0].click();", Dabtn)
	# driver.find_element_by_id("EXM0017").click()
	# time.sleep(1)

	semSub = find(5,"semesterSubId")
	semSub.click()
	# driver.find_element_by_name("semesterSubId").click()
	# get element through text
	el = find(1,"semesterSubId")
	# el = driver.find_element_by_id('semesterSubId')
	# op = find(6,"option")
	for option in el.find_elements_by_tag_name('option'):
		# print(option.text)
		if option.text == 'Fall Semester 2021-22':
			option.click() # select() in earlier versions of webdriver
			break
	time.sleep(10)

	tableRows = driver.find_element_by_tag_name("tr")
	for tablerow in tableRows:
		td = tablerow.find_element_by_tag_name("td")
		for i in td:
			print(i)

def HostelBooking():
	time.sleep(1)
	print("Click on Hostels")
	try:
		hostelbtn = find(2,"Hostels")
		# driver.find_element_by_link_text("Hostels").click()
		hostelbtn.click()
		online_booking = find(1,"HSL0112")
		# button = driver.find_element_by_id("HSL0112")
		driver.execute_script("arguments[0].click();", online_booking)
		# time.sleep(1)
	except:
		print("Hostel clicking failed")
		HostelBooking()




# This function converts all non black pixels to white
def refine(image,pixel_matrix):
	for col in range(0, image.height):
		for row in range(0, image.width):
			if pixel_matrix[row, col] != 0:
				pixel_matrix[row, col] = 255


# This function reduces noise by checking adjacent pixels of a black pixel
def noise_red(image,pixel_matrix):
	for col in range(1, image.height - 1):
		for row in range(1, image.width - 1):
			if pixel_matrix[row, col] == 0 and pixel_matrix[row, col - 1] != 0 and pixel_matrix[row, col + 1] != 0:
				pixel_matrix[row, col] = 255
			if pixel_matrix[row, col] == 0 and pixel_matrix[row - 1, col] != 0 and pixel_matrix[row + 1, col] != 0:
				pixel_matrix[row, col] = 255

def login():
	try:
		path = os.path.dirname(__file__)

		# Open the website
		driver.get('https://vtop.vit.ac.in/vtop')

		#Click on Login button
		# Find the button using text
		loginToVtopBtn = find(3,'//button[normalize-space()="Login to VTOP"]')
		loginToVtopBtn.click()

		#Find Username textbox
		user_box = find(1,'uname')
		user_box.send_keys("")#*********************Insert your Username in "" ***********************

		# Find password box
		pass_box = find(1,'passwd')
		pass_box.send_keys("")#*********************Insert your Password in "" ***********************

		#Captcha code
		try:
			# captcha_img = find(4,'[alt="vtopCaptcha"]')
			captcha_src = driver.find_element_by_css_selector('[alt="vtopCaptcha"]').get_attribute("src")
			# captcha_src = captcha_img.get_attribute("src")
			# download the image
			urllib.request.urlretrieve(captcha_src, "captcha.png")
			# opening and converting image to Grayscale
			image = Image.open("captcha.png").convert("L")
			pixel_matrix = image.load()

			refine(image,pixel_matrix)
			noise_red(image,pixel_matrix)

			# This part of code (to break Captcha) is work of @Presto412
			# -------------------------------------------------------------------
			characters = "123456789abcdefghijklmnpqrstuvwxyz"
			captcha = ""
			with open("bitmaps.json", "r") as fin:
				bitmap = json.load(fin)

				# parses every character, 6 is number of characters
				for j in range(int(image.width / 6), image.width + 1, int(image.width / 6)):
					char_img = image.crop((j - 30, 12, j, 44))
					char_matrix = char_img.load()
					matches = {}
					for char in characters:
						match = 0
						black = 0
						bitmap_matrix = bitmap[char]
						for col in range(0, 32):
							for row in range(0, 30):
								if char_matrix[row, col] == bitmap_matrix[col][row] \
									and bitmap_matrix[col][row] == 0:
									match += 1
								if bitmap_matrix[col][row] == 0:
									black += 1
						perc = float(match) / float(black)
						matches.update({perc: char[0].upper()})
					try:
						captcha += matches[max(matches.keys())]
					except ValueError:
						print("failed captcha")
						captcha += "0"
			# -------------------------------------------------------------------

				driver.find_element_by_id("captchaCheck").send_keys(captcha)
			# loginBtn = find(1,"captcha")
			# # driver.find_element_by_id("captcha").click()
			# loginBtn.click()
		except:
			print("No captcha available")
		loginBtn = find(1,"captcha")
		driver.execute_script("arguments[0].click();", loginBtn)
	except:
		print("************Failed. Trying again")
		login()

flag = 0
while(flag == 0):
	try:
		print("************Trying to login")
		login()
		print("*************Logged In")
		flag = 1
	except:
		print("************Failed. Trying again")
		login()
menu_toggle = find(1,'menu-toggle')
menu_toggle.click()
#DAUpload()
HostelBooking()

# for option in el.find_elements_by_tag_name('option'):
#     # print(option.text)
#     if option.text == 'Fall Semester 2021-22':
#         option.click() # select() in earlier versions of webdriver
#         break
# time.sleep(10)

# tableRows = driver.find_element_by_tag_name("tr")
# for tablerow in tableRows:
#     td = tablerow.find_element_by_tag_name("td")
#     for i in td:
#         print(i)
# foreach(var tableRow in tableRows)
# {
#    var td = tableRow.FindElements(By.TagName("td"));
#    if(td[2].Text.Contains("hi"))
#    {
#       td[0].FindElement(By.TagName("a")).Click();
#    }
# }
