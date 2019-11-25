import requests
from bs4 import BeautifulSoup
import unicodedata

def scrapper(keyWord):
	base_url = 'http://catalog.habib.edu.pk/cgi-bin/koha/opac-search.pl?q=&submit=Submit'
	keyword = ''
	for i in keyWord:
		if i == ' ':
			i = '+'
		keyword += i
		
	#creating the base url:
	url = base_url[:-14] + keyword + base_url[-14:]

	# sending and recieving the request
	r = requests.get(url)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')


	# extracting books
	books = soup.findAll('a',{'class':'title'})

	out = []
	for i in books:
		t = unicodedata.normalize("NFKD", i.text)
		out.append(t)

	return out