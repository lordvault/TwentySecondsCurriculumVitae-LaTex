import sys
import os
from linkedin_scraper import actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from python.Persone import Persone

def scrape_linked_in_info():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
    driver = webdriver.Chrome(sys.argv[3], options=chrome_options)

    email = sys.argv[1]
    password = sys.argv[2]
    actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
    person = Persone("https://www.linkedin.com/in/jorge-montes/en", driver=driver)
    print(person.name)
    print(person.about)
    print(person.experiences)

    scrape_info = {
        "name": person.name,
        "about": person.about
    }
    return scrape_info
    

def replace_text_on_latex(scrape_info):
    if os.path.exists("Twenty-Seconds_cv_re.tex"):
        print("Deleting file Twenty-Seconds_cv_re.tex")
        os.remove("Twenty-Seconds_cv_re.tex")
    fin = open("Twenty-Seconds_cv.tex", "rt", encoding="utf-8")
    fout = open("Twenty-Seconds_cv_re.tex", "wt", encoding="utf-8")
    for line in fin:
        fout.write(line.replace('==NAME==', scrape_info["name"]))
        fout.write(line.replace('==ABOUT_ME==', scrape_info["about"][0]))
    fin.close()
    fout.close()

replace_text_on_latex(scrape_linked_in_info())

exit()
