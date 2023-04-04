from bs4 import BeautifulSoup
import requests
import os

def getFD(url):
	page = requests.get(url).text
	soup = BeautifulSoup(page, 'html.parser')
	hrefs = []
	for node in soup.find_all('a'):
		if str(node.get('href'))[0] == '/':
			hrefs.append(node.get('href'))
	return hrefs

def delURLDir(text):
	temp = text[1:]
	index = temp.find('/')
	if index == -1:
		return text
	else:
		return temp[index+1:]

def getURLDir(text):
	temp = text[1:]
	index = temp.find('/')
	if index == -1:
		return None
	else:
		return temp[:index]

cwd = os.getcwd()
URL = input('URL (do NOT include https://)\n  > ').lower()
finalURL = 'https://' + URL
page = requests.get(finalURL)
if not os.path.exists(cwd+f'/HTMLs/{URL}'):
	os.mkdir(cwd+f'/HTMLs/{URL}')

more = input('Would you like to search other directories? (y/n)\n  > ').lower()
if more == 'y':
	hrefs = getFD(finalURL)
	if '/' in hrefs:
		hrefs.remove('/')
	URLs = [finalURL + href for href in hrefs]
	
	filename = cwd + f'/HTMLs/{URL}/{URL}.html'
	with open(filename, 'w') as f:
		f.write(page.text)
		
	for href in hrefs:
		dir = getURLDir(href)
		if dir != None:
			if not os.path.exists(cwd+f'/HTMLs/{URL}/{dir}'):
				os.mkdir(cwd+f'/HTMLs/{URL}/{dir}')
			delURLDir(href)
		
	for i in range(len(URLs)):
		page = requests.get(URLs[i])
		filename = cwd + f'/HTMLs/{URL}{hrefs[i]}.html'
		with open(filename, 'w') as f:
			f.write(page.text)
			
else:
	filename = cwd + f'/HTMLs/{URL}.html'
	with open(filename, 'w') as f:
		f.write(page.text)