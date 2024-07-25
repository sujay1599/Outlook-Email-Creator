import yaml
import random
import time
import os
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import logging

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def random_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))

def log_account_details(username, password):
    with open('data/accounts_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f"{username}@outlook.com", password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def create_account(driver, first_name, last_name, username, password, birth_year, birth_month, birth_day):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'usernameInput')))
        random_delay()
        driver.find_element(By.ID, 'usernameInput').send_keys(username)
        random_delay()
        driver.find_element(By.ID, 'usernameInput').send_keys('\n')

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'Password')))
        random_delay()
        driver.find_element(By.NAME, 'Password').send_keys(password)
        random_delay()
        driver.find_element(By.NAME, 'Password').send_keys('\n')

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'firstNameInput')))
        random_delay()
        driver.find_element(By.ID, 'firstNameInput').send_keys(first_name)
        random_delay()
        driver.find_element(By.ID, 'lastNameInput').send_keys(last_name)
        random_delay()
        driver.find_element(By.ID, 'lastNameInput').send_keys('\n')

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'BirthDay')))
        random_delay()
        
        select_month = Select(driver.find_element(By.ID, 'BirthMonth'))
        select_month.select_by_value(str(birth_month))
        random_delay()
        
        select_day = Select(driver.find_element(By.ID, 'BirthDay'))
        select_day.select_by_value(str(birth_day))
        random_delay()
        
        driver.find_element(By.ID, 'BirthYear').send_keys(str(birth_year))
        random_delay()
        driver.find_element(By.ID, 'BirthYear').send_keys('\n')

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'declineButton')))
            random_delay()
            driver.find_element(By.ID, 'declineButton').click()
        except Exception as e:
            logging.warning(f"Decline button not found or not needed: {e}")

        try:
            captcha_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'captcha-container')))
            logging.info("CAPTCHA detected. Please solve it manually and press Enter to continue...")
            input("Press Enter after solving the CAPTCHA...")
        except:
            pass

        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'mainApp')))
        except Exception as e:
            logging.error(f"Main app not found: {e}")

        log_account_details(username, password)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error(driver.page_source)

def setup_proxy(chrome_options, proxy):
    if "@" in proxy:
        proxy_auth, proxy_ip = proxy.split("@")
        username, password = proxy_auth.split(":")
        ip, port = proxy_ip.split(":")
    else:
        username, password = None, None
        ip, port = proxy.split(":")

    if username and password:
        chrome_options.add_argument(f"--proxy-server={ip}:{port}")
        chrome_options.add_argument(f'--proxy-auth={username}:{password}')
    else:
        chrome_options.add_argument(f"--proxy-server={ip}:{port}")

def main():
    config = load_config()

    width = 1920
    height = 1080

    chrome_options = Options()
    chrome_options.add_argument(f'--window-size={width},{height}')
    chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    if 'PROXIES' in config and config['PROXIES']:
        proxy = random.choice(config['PROXIES'])
        setup_proxy(chrome_options, proxy)

    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')  # Ensure correct file name for Windows
    
    # Check if chromedriver exists at the specified path
    if not os.path.isfile(chromedriver_path):
        logging.error(f"Chromedriver not found at path: {chromedriver_path}")
        return

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(width, height)
    driver.get('https://outlook.live.com/owa/?nlp=1&signup=1')

    if config.get('AUTO_CREATE', True):
        with open('names.txt', 'r') as f:
            names = f.read().splitlines()

        with open('words5char.txt', 'r') as f:
            words = f.read().splitlines()

        for _ in range(config['NUMBER_OF_ACCOUNTS']):
            random_first_name = random.choice(names).strip()
            random_last_name = random.choice(names).strip()
            username = random_first_name + random_last_name + str(random.randint(1000, 9999))

            first_word = random.choice(words).strip()
            second_word = random.choice(words).strip()
            random_password = first_word + second_word + '!'

            birth_year = random.randint(1990, 1999)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)

            create_account(driver, random_first_name, random_last_name, username, random_password, birth_year, birth_month, birth_day)
    else:
        first_names = config['FIRST_NAMES']
        last_names = config['LAST_NAMES']
        user_passwords = config['USER_PASSWORDS']
        for i in range(config['NUMBER_OF_ACCOUNTS']):
            first_name = first_names[i % len(first_names)]
            last_name = last_names[i % len(last_names)]
            password = user_passwords[i % len(user_passwords)]
            username = first_name + last_name + str(random.randint(1000, 9999))
            create_account(driver, first_name, last_name, username, password, config['BIRTH_YEAR'], config['BIRTH_MONTH'], config['BIRTH_DAY'])

    driver.quit()

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')

    log_file_path = 'data/accounts_log.csv'
    if not os.path.exists(log_file_path):
        with open(log_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Password", "Created On"])

    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
