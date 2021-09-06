import sys
from linkedin_scraper import Person, actions
from selenium import webdriver

from Persone import Persone

driver = webdriver.Chrome('./chromedriver')

email = sys.argv[1]
password = sys.argv[2]
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Persone("https://www.linkedin.com/in/jorge-montes/en", driver=driver)
print(person.name)
print(person.about)
print(person.experiences)
