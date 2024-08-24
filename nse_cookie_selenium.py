import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import configparser
from datetime import datetime, timedelta

# Initialize the current timestamp
current_timestamp = datetime.now()
load_dttm = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

# URL to visit
url = 'https://www.nseindia.com/market-data/live-market-indices'

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode if needed
chrome_options.add_argument("--window-size=1280,720")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')

# Initialize the WebDriver using the ChromeDriverManager to install the Chrome driver automatically
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set extra headers (This may require a workaround as Selenium doesn't natively support setting headers easily)
driver.get(url)

# Wait until the page has fully loaded
time.sleep(5)  # Or use WebDriverWait if waiting for specific elements

# Get cookies
cookies = driver.get_cookies()
cookie_string = ''
for cookie in cookies:
    cookie_string += f"{cookie['name']}={cookie['value']};"

# Load and write to the config file
config = configparser.ConfigParser(interpolation=None)
config.read('credentials.ini')
config['nse_cookie']['cookie'] = cookie_string
config['nse_cookie']['load_dttm'] = load_dttm

with open('credentials.ini', 'w') as configfile:
    config.write(configfile)

# Close the browser
driver.quit()
sys.exit(0)
