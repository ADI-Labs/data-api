import re
import robobrowser
import json

from robobrowser import RoboBrowser


browser = RoboBrowser()


url = 'https://cas.columbia.edu/cas/login?TARGET=' + \
	'https%3A%2F%2Fdirectory.columbia.edu%2Fpeople%2F' + \
	'browse%2Fstudents%3Ffilter.lnameFname%3D2%26filter.initialLetter%3DA'



#get login information from config file in root directory
config = json.load(open('../config.json'))
LOGIN = config['login']
uni = LOGIN['uni']
password = LOGIN['password']


#open login page
browser.open(url)
login = browser.get_form()

#use credentials from file
login['username'] = uni
login['password'] = password
browser.submit_form(login)



browser.select('.table_results')

browser.parsed()







