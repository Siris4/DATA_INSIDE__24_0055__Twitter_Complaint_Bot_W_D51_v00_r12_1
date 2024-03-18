import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import re

element_for_Total_Play_speed = '''
<a class="no-link-chev btnBanner" href="/personaliza?150#internet" promo-name="150 megas 2p" promo-id="1" target="_blank">
    <img class="d-none d-md-block w-100" src="/assetsv2/img/home/sliders/Banner1.png">
    <img class="d-block d-md-none" src="/assetsv2/img/home/sliders/Banner1_mobile.png">
</a>'''

# the regular expression pattern to extract out the number of Mbps (megas):
# pattern = r'promo-name="(\d+ megas)'  # this one is a string
pattern = r'promo-name="(\d+)'  # this is an integer

# Search for the pattern in the string
match = re.search(pattern, element_for_Total_Play_speed)

# Check if a match was found
if match:
    extracted_text = match.group(1)
    # print(extracted_text)
else:
    extracted_text = "No internet speed found."

# CONSTANTS:
PROMISED_SPEEDS_DOWN = extracted_text
PROMISED_SPEEDS_UP = 10

# print(
#     f"\nThis is the first print statement and shows the integer of the extracted text, which is then converted to PROMISED_SPEEDS_DOWN: {int(PROMISED_SPEEDS_DOWN)}")

TWITTER_EMAIL = "YOUR_EMAIL"
TWITTER_PASSWORD = "YOUR_PASSWORD"

URL_FOR_SPEEDTEST = "https://www.speedtest.net/"


# ChromeDriverManager is handled by the webdriver_manager.chrome


class InternetSpeedTwitterBot:
    def __init__(self, PROMISED_SPEEDS_DOWN, PROMISED_SPEEDS_UP):
        # driver = init_driver()  #try this 1st
        self.driver = self.init_driver()
        self.PROMISED_SPEEDS_DOWN = PROMISED_SPEEDS_DOWN
        self.PROMISED_SPEEDS_UP = PROMISED_SPEEDS_UP

        self.open_website(URL_FOR_SPEEDTEST)
        self.get_internet_speed()
        self.tweet_at_provider()

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        self.log_message("webdriver initialized.")
        return driver

    # my function to log messages:
    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{timestamp} - {message}")


    def print_test_for_megas_speed(self, PROMISED_SPEEDS_DOWN, PROMISED_SPEEDS_UP):
        self.log_message(
            f"The Promised Download speed which is stated on Total Play's Website is: {PROMISED_SPEEDS_DOWN} (Mbps)")
        self.log_message(
            f"The Promised Upload speed which is stated on Total Play's Website is: {PROMISED_SPEEDS_UP} (Mbps)")


    def open_website(self, url):
        self.driver.get(URL_FOR_SPEEDTEST)
        self.log_message(f"Successfully opened the website: {URL_FOR_SPEEDTEST}")

        self.print_test_for_megas_speed(self.PROMISED_SPEEDS_DOWN, self.PROMISED_SPEEDS_UP)

        time.sleep(2)



    def get_internet_speed(self):
        XPATH_fpr_speed_url = '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]'
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, XPATH_fpr_speed_url))
        )
        self.speed_button = self.driver.find_element(By.XPATH, XPATH_fpr_speed_url)
        self.speed_button.click()  # clicks on the Go button to generate the speeds
        print("The Go button was pushed to start the Internet Speed Test.")

        # Go button:
        # CSS_selector_for_speed_URL = ".start-text"
        # element_for_speed_url = '<span class="start-text">Go</span>'

    def tweet_at_provider(self):
        pass



# creating an instance of internetspeedtwitterbot:
TwitterBot = InternetSpeedTwitterBot(PROMISED_SPEEDS_DOWN, PROMISED_SPEEDS_UP)

# we can now call the methods on the instance that was created just above
# TwitterBot.open_website(URL_FOR_SPEEDTEST)

TwitterBot.tweet_at_provider()


