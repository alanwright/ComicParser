from BeautifulSoup import BeautifulSoup
import urllib2
import json

DOMAIN = 'http://leagueofcomicgeeks.com/'
DETAIL_SPLIT = '&nbsp;&#183;&nbsp;'

class Comic:
	def __init__(self, title = None, publisher = None, releaseDate = None, price = None, thumbnail = None, image = None):
		self.title = title
		self.publisher = publisher
		self.releaseDate = releaseDate
		self.price = price
		self.thumbnail = thumbnail
		self.image = image

	def __str__(self):
		return "Title: %s\nPublisher: %s\nRelease Date: %s\nPrice: %s\nThumbnail: %s\nImage: %s" % (self.title, self.publisher, self.releaseDate, self.price, self.thumbnail, self.image) 

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


#Fetch page and releases
html = urllib2.urlopen('http://leagueofcomicgeeks.com/comics/new-comics')
homepage_parsed_html = BeautifulSoup(html)
entries = homepage_parsed_html.body.findAll('li', attrs={'class':'media'})

print 'Found', len(entries), 'new release entries'

comics = []
comics_JSON = '{"comics":'
for entry in entries:
	comic = Comic()

	#Parse title
	comic.title = entry.find('div', attrs={ 'class':'comic-title'}).text

	comic_details = entry.find('div', attrs={ 'class':'comic-details comic-release'}).text.split(DETAIL_SPLIT)
	comic.publisher = comic_details[0]
	comic.releaseDate = comic_details[1]
	if len(comic_details) > 2:
		comic.price = comic_details[2]

	#Parse images
	comic.thumbnail = DOMAIN + entry.find('img').get('src')
	comic.image = comic.thumbnail.replace("medium", "large")

	#Print and save comic json
	print comic
	comics.append(comic)
	comics_JSON = comics_JSON + str(comic.to_JSON()) + ','

#Write out json to file
comics_JSON = comics_JSON + '}'
with open('comics.json', 'w') as outfile:
	outfile.write(comics_JSON)	