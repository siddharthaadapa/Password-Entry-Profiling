from selenium import webdriver
from getpass import getpass

username = input("Enter your Username:")
password = getpass("Enter in your Password:")

driver = webdriver.Chrome("C:\\Users\\hp\Desktop\\Capstone\\selenium\\chromedriver.exe")
driver.get("http://127.0.0.1/login")

username_textbox = driver.find_element_by_id("email")
username_textbox.send_keys(username)

password_textbox = driver.find_element_by_id("password")
password_textbox.send_keys(password)

login_button = driver.find_element_by_id("login")
login_button.click()