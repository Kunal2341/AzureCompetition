from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import json
from math import sin, cos, sqrt, atan2, radians
def findLatLongOfCollege(collegeNameInputed):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.google.com/maps/")
    inputTxT = "/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/form/div/div[3]/div/input[1]"
    collegeName1 = "/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]"
    collegeName2 = "/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[3]/div[1]/div[1]/div[1]/h1/span[1]"
    collegeName3 = "/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/h1/span[1]"
    driver.find_element_by_xpath(inputTxT).send_keys(Keys.CONTROL, 'a')
    driver.find_element_by_xpath(inputTxT).send_keys(collegeNameInputed)
    driver.find_element_by_xpath(inputTxT).send_keys(Keys.ENTER)
    time.sleep(10)
    try:
        collegeName = driver.find_element_by_xpath(collegeName1).text
    except Exception as e:
        try:
            collegeName = driver.find_element_by_xpath(collegeName2).text
        except Exception as e:
            collegeName = driver.find_element_by_xpath(collegeName3).text
    link = driver.current_url
    driver.quit()
    CollegeNameExtracted =link[34:34+link[34:].find("/")].replace("+", " ")
    lat = link[link.find("@")+1:].split(",")[0]
    long = link[link.find("@")+1:].split(",")[1]
    if collegeName != CollegeNameExtracted:
        print("College Name and College Name Extracted are different")
    print("College Name: " + collegeName)
    print("College Name Extracted: " + collegeName)
    print("Lat: " + str(lat) + "\tLong: " + str(long))
    return lat,long,collegeName


lat, long, collegeName = findLatLongOfCollege("Georgia Tech")
lat =  float(lat)
long = float(long)
