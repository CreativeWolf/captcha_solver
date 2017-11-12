from selenium import webdriver
from subprocess import call
from time import sleep
from os import remove

#==========================================
#	for thresholding image
#==========================================
import cv2
import numpy as np

l = ["word.txt","temp.png","thresholded.jpg"]
for i in l:
	try:
		remove(i)
	except:
		continue

def threshold(path):
	img = cv2.imread(path)
	grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	retval2,threshold2 = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# cv2.imshow('original',img)
	# cv2.imshow('Otsu threshold',threshold2)
	cv2.imwrite("thresholded.jpg",threshold2)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
#==========================================


class aadhaar_api():

	def __init__(self):
		self.browser = webdriver.Firefox()

	def save_screenshot_of_element(self,element):
		element.screenshot("./temp.png")
		threshold("./temp.png")		#global function

	def check_captcha(self,path):
		f = open(path,"r")
		con = f.read().strip()
		
		if con.isdigit():
			f.close()
			print "captcha: ",con
			return True
		f.close()
		return False 

	def get_captcha_text(self):
		self.browser.get("https://resident.uidai.gov.in/aadhaarverification")
		img = self.browser.find_element_by_xpath('//img[@alt="Text to Identify"]')
		reload = self.browser.find_element_by_class_name("captcha-reload")

		self.save_screenshot_of_element(img)
		call(["tesseract","thresholded.jpg","word"])
		print "Initail files saved"
		sleep(0.1)

		while not self.check_captcha("word.txt"):
			reload.click()
			sleep(0.1)
			self.save_screenshot_of_element(img)
			sleep(0.1)
			
		self.close_browser()		

	def close_browser(self):
		self.browser.close()

	def test(self):
		self.browser.get("https://resident.uidai.gov.in/aadhaarverification")
		for i in range(20):
			img = self.browser.find_element_by_xpath('//img[@alt="Text to Identify"]')
			self.save_screenshot_of_element(img)
			reload = self.browser.find_element_by_class_name("captcha-reload")
			reload.click()

		self.close_browser()		



if __name__ == "__main__":
	API = aadhaar_api()
	API.get_captcha_text()
	# API.test()