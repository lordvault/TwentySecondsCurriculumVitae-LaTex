import sys
import actione
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Persone import Persone

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)

email = sys.argv[1]
password = sys.argv[2]
actione.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Persone("https://www.linkedin.com/in/jorge-montes/en", driver=driver)
print(person.name)
print(person.about)
print(person.experiences)
exit()
