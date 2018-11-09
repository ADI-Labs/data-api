#!/usr/bin/env python
import re
import robobrowser
import json
import time

from robobrowser import RoboBrowser


initial_url = 'https://cas.columbia.edu/cas/login?TARGET=' + \
	'https%3A%2F%2Fdirectory.columbia.edu%2Fpeople%2F' + \
	'browse%2Fstudents%3Ffilter.lnameFname%3D2%26filter.initialLetter%3DA'


url_base = 'https://directory.columbia.edu'
browse_url = url_base + '/people/browse/students'

#get login information from config file in root directory
config = json.load(open('../app/config.json'))
LOGIN = config['login']
uni = LOGIN['uni']
password = LOGIN['password']



#Array that stores JSON objects containing student data
students = []


def replace_breaks(item, delimiter):
	for br in item.find_all('br'):
		br.replace_with(delimiter)

	return item



# Stores student information in students array
# Creates a JSON object form Python dictionary in the following format
#	
#	{'Name': <student name>, 'Address': <address>, 'Email': <email>, 'Phone': <phone>}
#

def parse_information(rows):

	info = {
				'Name': True, \
				'UNI': True, \
				'Email': True, \
				'Department': True, \
				'Title': True, \
				'Address': True, \
				'Home Addr': True,
				'Campus Tel': True, \
				'Tel': True
			}

	# print(rows)



	# data = person.find_all('td')

	for row in rows:
		name = row.find('th')

		# This means that it is table header which contains name
		if name == None:

		 	items = row.find_all('td')
		 	field = None
		 	for item in items:

		 		print(item.find(class_='align_rb'))

		 		txt = item.text
		 		
		 		if ':' in txt and info[txt.replace(':', '')] == True:
		 			field = 

		 		# if txt != '\u00a0' and txt != '':
		 		# 	info[field] = txt


		else:
		 	info['Name'] = name.text








	# #Get name
	# info['Name'] = data[0].text


	# #Get department and title
	# information = data[1].find_all('div')
	# for field in information:
	# 	field = replace_breaks(field, ' ')
	# 	text = field.text
	# 	fields = text.split(':')
	# 	info[fields[0]] = fields[1]


	# #Get address
	# if data[2].text != None:
	# 	info['Address'] = replace_breaks(data[2], ' ').text
	# else:
	# 	info['Address'] = ''



	# #Get email and phone number
	# contact_info = replace_breaks(data[3], ':').text
	# contact_info = contact_info.split(':')
	
	# #Has email and phone number
	# if len(contact_info)==2:
	# 	info['Email'] = contact_info[0]
	# 	info['Phone'] = contact_info[1]
	# else:
	# 	info['Email'] = contact_info[0]


	# for key, value in info.items():
	# 	if value == '\u00a0':
	# 		info[key] = ''

	students.append(info)



# For each alphabetical character, this visits each webpage and gets a table which contains student information
def get_data(browser):
	pages = browser.find(class_='page_number_result').find_all('a')
	last_page = pages[len(pages)-1]['href']
	last_page = last_page.split('=')

	num_pages = int(last_page[len(last_page)-1])
	query_format = '?page='

	# for pageNumber in range(0, num_pages+1):
	# 	url = url_base + query_format + str(pageNumber)
	# 	browser.open(url)

	table = browser.find(class_='table_results')	
	people = table.find_all('tr')
			
	links = []
	#The first table row (0th element of array) is always the row containing the labels
	for integer in range(1, len(people)):
		link = people[integer].find_all('a')
		if len(link) > 0:
			links.append(url_base+link[0]['href'])

	while len(links)!=0:
		link = links.pop(0)
		browser.open(link)
		rows = browser.find(class_='table_results_indiv').find_all('tr')
		# print(rows)
		parse_information(rows)
		break


def writeFile():
	#open data json file
	file = open('student_data.json', 'w')

	numStudents = len(students)
	file.write('[\n')
	for index in range(numStudents):
		file.write(json.dumps(students[index], indent=4))
		if index == numStudents-1:
			file.write('\n')
		else:
			file.write(',\n')
	file.write(']')
	file.close()




if __name__=='__main__':

	browser = RoboBrowser()

	#open login page
	browser.open(initial_url)
	login = browser.get_form()

	#use credentials from file
	login['username'] = uni
	login['password'] = password
	browser.submit_form(login)


	print('Getting data from ', initial_url)
	#Get data for first letter
	get_data(browser)
	print(students)
	# pages = browser.find(class_='name_form_az').find_all('a')


	# #This gets the links to each intial web page (i.e page 0) that contains a query for an alphabetical character
	# web_pages = []
	# for page in pages:
	# 	if page.has_attr('href'):
	# 		web_pages.append(page['href'])


	# #This iterates through each web page
	# for page in web_pages:
	# 	time.sleep(5)
	# 	url = browse_url+page
	# 	print('Getting data from ', url)
	# 	browser.open(url)
	# 	get_data(browser)


	# writeFile()
