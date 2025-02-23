from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from subprocess import call, PIPE
from time import sleep
from os import remove
import cv2
import numpy as np

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#==========================================
#	for thresholding image
#==========================================
# def threshold(path):
# 	img = cv2.imread(path)
# 	grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# 	retval2,threshold2 = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# 	# cv2.imshow('original',img)
# 	# cv2.imshow('Otsu threshold',threshold2)
# 	cv2.imwrite("thresholded.jpg",threshold2)
# 	# cv2.waitKey(0)
# 	# cv2.destroyAllWindows()
# #==========================================


class aadhaar_api():

	def __init__(self):
		self.init_clean()
		self.browser = webdriver.Firefox()
		self.captcha_text = None

	def save_screenshot_of_element(self,element):
		element.screenshot("./temp.png")
		sleep(0.1)
		
		img = cv2.imread("./temp.png")
		grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		retval2,threshold2 = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		cv2.imwrite("thresholded.jpg",threshold2)
		sleep(0.1)

	def check_captcha(self,path):
		f = open(path,"r")
		self.captcha_text = f.read().strip()
		# print self.captcha_text
		
		if self.captcha_text.isdigit():
			f.close()
			# print "captcha: ",self.captcha_text
			return True
		f.close()
		return False 

	def get_captcha_text(self):
		self.browser.get("https://resident.uidai.gov.in/aadhaarverification")
		img = self.browser.find_element_by_xpath('//img[@alt="Text to Identify"]')
		reload = self.browser.find_element_by_class_name("captcha-reload")

		self.save_screenshot_of_element(img)
		call(["tesseract","thresholded.jpg","word"])
		# print "Initail files saved"
		sleep(0.1)

		while not self.check_captcha("word.txt"):
			reload.click()
			sleep(0.1)
			self.save_screenshot_of_element(img)
			call(["tesseract","thresholded.jpg","word"])
			sleep(0.1)
			
	def authenticate_aadhaar(self,aadhaar_no):
		assert self.captcha_text.isdigit()

		aadhaar_textfield = self.browser.find_element_by_id("uid")
		aadhaar_textfield.clear()
		aadhaar_textfield.send_keys(aadhaar_no)
		aadhaar_textfield.send_keys(Keys.RETURN)



		captcha = self.browser.find_element_by_id("_aadhaarverification_WAR_AadhaarVerificationportlet_captchaText")
		captcha.clear()
		captcha.send_keys(self.captcha_text)
		captcha.send_keys(Keys.RETURN)

		element = WebDriverWait(self.browser, 10).until(
        	EC.presence_of_element_located((By.NAME, "Verify Another Aadhaar"))
    	)

		result = self.browser.find_elements_by_tag_name('h2')[2]
		# result = self.browser.find_element_by_xpath('//h2[@class="floatLeft marginTop50 fontSize15 fontWeightBold color333333 textAlignCenter width100"]')
		print result.text
		if result.text.find("Exists") != -1:
			print "True"
			return True
		print "False"
		return False


	def close_browser(self):
		self.browser.close()

	def init_clean(self):
		l = ["word.txt","temp.png","thresholded.jpg"]		#initial file cleanup
		for i in l:
			try:
				remove(i)
			except:
				continue

	# def test(self):
	# 	self.browser.get("https://resident.uidai.gov.in/aadhaarverification")
	# 	for i in range(20):
	# 		img = self.browser.find_element_by_xpath('//img[@alt="Text to Identify"]')
	# 		self.save_screenshot_of_element(img)
	# 		reload = self.browser.find_element_by_class_name("captcha-reload")
	# 		reload.click()

	# 	self.close_browser()		



if __name__ == "__main__":
	API = aadhaar_api()
	API.get_captcha_text()
	API.authenticate_aadhaar("291560455557")
	API.get_captcha_text()
	API.authenticate_aadhaar("952489062216")
	API.get_captcha_text()
	API.authenticate_aadhaar("952489452216")
	API.init_clean()
	# API. close_browser()