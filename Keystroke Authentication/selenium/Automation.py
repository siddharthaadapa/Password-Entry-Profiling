from selenium import webdriver
from getpass import getpass

username = input("Enter your Username:")
password = getpass("Enter in your Password:")

driver = webdriver.Chrome("C:\\Users\\hp\Desktop\\Capstone\\selenium\\chromedriver.exe")
driver.get("http://127.0.0.1/register")

username_textbox = driver.find_element_by_id("email1")
username_textbox.send_keys(username)

password_textbox = driver.find_element_by_id("password1")
password_textbox.send_keys(password)

username_textbox = driver.find_element_by_id("email2")
username_textbox.send_keys(username)

password_textbox = driver.find_element_by_id("password2")
password_textbox.send_keys(password)

username_textbox = driver.find_element_by_id("email3")
username_textbox.send_keys(username)

password_textbox = driver.find_element_by_id("password3")
password_textbox.send_keys(password)

login_button = driver.find_element_by_id("register")
login_button.click()


