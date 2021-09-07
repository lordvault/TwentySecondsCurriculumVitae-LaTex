import sys
from linkedin_scraper import actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Persone import Persone

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


fin = open("Twenty-Seconds_cv.tex", "rt")
#output file to write the result to
fout = open("Twenty-Seconds_cv_re.tex", "wt")
#for each line in the input file
for line in fin:
	#read replace the string and write to output file
	fout.write(line.replace('pyton', 'python'))
#close input and output files
fin.close()
fout.close()

exit()
