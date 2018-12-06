#!/usr/bin/env python
import json
import time
from robobrowser import RoboBrowser



# URLs that are used to scrape.
login_url = 'https://cas.columbia.edu/cas/login?TARGET=' + \
	'https%3A%2F%2Fdirectory.columbia.edu%2Fpeople%2F' + \
	'browse%2Fstudents%3Ffilter.lnameFname%3D2%26filter.initialLetter%3DA'
url_base = 'https://directory.columbia.edu'
browse_url = url_base + '/people/browse/students'


#get login information from config file in root directory
file = open('../app/config.json')
config = json.load(file)
file.close()


LOGIN = config['login']
uni = LOGIN['uni']
password = LOGIN['password']



MAX_NUM = 500 # Max number of people to scrape in a data
# WAIT_TIME = 86400 # Want the script to scrape portions in day intervals
WAIT_TIME = 90





'''
	
	This is the driver function which scrapes the Columbia directory for student data

	Parameters:
		None

'''
def scrape():

	browser = RoboBrowser()

	login(browser)

	pages = browser.find(class_='name_form_az').find_all('a')

	#This gets the links to each intial web page (i.e page 0) that contains a query for an alphabetical character
	web_pages = []
	for page in pages:
		if page.has_attr('href'):
			web_pages.append(page['href'])


	initializeFile()
	#Array that stores JSON objects containing student data
	students = []

	#Get data for first letter
	print('Getting data from ', login_url)
	getData(browser, students)

	#This iterates through each web page
	while len(web_pages) != 0:
		
		url = browse_url + web_pages.pop(0)

		print('Getting data from ', url)
		browser.open(url)
		getData(browser, students)





'''
	
	This function logs into the Columbia directory using the credentials file
	in project root directory

	Parameters:
		browser - RoboBrowser object

'''
def login(browser):
	#open login page
	browser.open(login_url)
	login = browser.get_form()

	#use credentials from file
	login['username'] = uni
	login['password'] = password
	browser.submit_form(login)





'''

	This function replaces breaks found in HTML text
	with a specified delimeter

	Parameters:

		item - BeautifulSoup object which contains HTML text
		delimiter - String to replace br

'''

def replaceBreaks(item, delimiter):
	for br in item.find_all('br'):
		br.replace_with(delimiter)
	return item





'''
	
	This function gets the email address which is an HTML link

	Parameters:

		text - BeautifulSoup object which contains HTML text

'''
def getAddr(text):
	addr = text.find_all('a')[0]
	return addr.text




'''

	This gets all of the student information found on a particular
	web page

	Parameters:

		rows - Array of BeautifulSoup objects which represents table rows
		students - Array of dictionaries which represent students and their information

'''
def parseInfo(rows, students):

	info = {
				'Name': '', \
				'UNI': '', \
				'Email': '', \
				'Department': '', \
				'Title': '', \
				'Address': '', \
				'Home Addr': '',
				'Campus Tel': '', \
				'Tel': '', \
				'FAX': ''
	}


	for row in rows:

		if info['Name'] == '' or info['Name'] == None:
			name = row.find('th')
			info['Name'] = name.text

		else:

		 	items = row.find_all('td')
		 	field = None

		 	#Every other td is a data field
		 	count = 0

		 	for item in items:

		 		txt = item.text
		 		
		 		if txt != '\u00a0' and txt != '':

		 			if count==0 and ':' in txt:
		 				txt = txt.replace(':', '')
		 				count += 1
		 				if info[txt] == '':
		 					field = txt
		 				else:
		 					continue

		 			elif count==1:

		 				if field == 'Email':
		 					txt = getAddr(item)
		 				elif field == 'Address':
		 					txt = replaceBreaks(item, ' ').text
		 				elif field == 'Campus Tel':
		 					temp = ''
		 					for index in range(len(txt)):
		 						if txt[index] == '\xa0':
		 							break
		 						temp += txt[index]

		 					txt = temp



		 				info[field] = txt
		 				count -= 1


	students.append(info)





'''
'''
def getData(browser, students):


	pages = browser.find(class_='page_number_result').find_all('a')
	last_page = pages[len(pages)-1]['href']
	last_page = last_page.split('=')

	num_pages = int(last_page[len(last_page)-1])
	query_format = '?page='

	for pageNumber in range(0, num_pages+1):
		url = browse_url + query_format + str(pageNumber)
		browser.open(url)

		table = browser.find(class_='table_results')

		people = table.find_all('tr')
				
		links = []
		
		for integer in range(1, len(people)):
			link = people[integer].find_all('a')
			if len(link) > 0:
				links.append(url_base + link[0]['href'])

		while len(links)!=0:

			if len(students) == MAX_NUM:
				writeToFile(students)

				students.clear()
				print('students len: ' +  str(len(students)))
				print(students)

				#For debugging purposes
				print('Sleeping for ' + str(WAIT_TIME) + ' seconds')
				time.sleep(WAIT_TIME)
				print('Continuing')
				# login(browser)


			link = links.pop(0)
			browser.open(link)
			rows = browser.find(class_='table_results_indiv').find_all('tr')
			parseInfo(rows, students)



'''
	
	This method writes the array of students and their information to 
	a JSON file as an array of JSON objects

	Parameters:

		students - Array of dictionaries which contain student information

'''
def writeToFile(students):
	#open data json file
	file = open('student_data.json', 'ab+')
	

	#Checks to see if file has already be written to. If so, append json data
	file.seek(0,2)
	if file.tell() == 0:
		file.write(json.dumps(students, indent=4).encode())

	else:
		file.seek(-1,2)
		file.truncate()
		file.write(' , '.encode())
		file.write(json.dumps(students, indent=4).encode())
		file.write(']'.encode())

	file.close()





'''
	
	Creates a file called "student_data.json" or overwrites the file if it
	already exists

	Parameters:
		None

'''
def initializeFile():
	file = open('student_data.json', 'w')
	file.close()


if __name__=='__main__':
	scrape()