from lxml import html
import datetime
import requests

def parse_netflix(file_name):

	netflix = open(file_name, 'r')
	text = netflix.read()
	tree = html.fromstring(text)
	lyst = tree.find_class("retableRow")
	history = {}
	format = '%m/%d/%Y'

	for elem in lyst:
		x = elem.text_content().encode('utf-8').strip()
		y = x.split("Report")[0]
		z = y.split("/")

		month = z[0]
		day = z[1]
		year = '20' + z[2][0:2]
		title = z[2][2:]

		if "Season" in title:
			terms = title.split(":")
			show_name = terms[0]
			episode = terms[2].replace('"', "").replace(" ", "").replace("\\", "")
			request = 'https://itunes.apple.com/search?term=' + episode + '&artistName=' + show_name + '&entity=tvEpisode'

		else:
			request = 'https://itunes.apple.com/search?term=' + title + '&entity=movie'

		r = requests.get(request)

		try:
			content_length = 0
			for result in r.json()['results']:
				if result['artistName'] == show_name:
					content_length += round(float(r.json()['results'][0]['trackTimeMillis'])/60000, 0)
					break
		except:
			content_length = 0

		if content_length == 0:

			wiki_req = "https://en.wikipedia.org/wiki/" + show_name.replace (" ", "_")

			page = requests.get(wiki_req)
			if page.status_code == 200:
				tree = html.fromstring(page.text)
				try:
					info = tree.find_class('infobox vevent')[0]
					for elem in info:
						if "Running time" in elem.text_content():
							time = elem.text_content().encode('utf-8')
							content_length += float(time.split("\n")[2][0:2])
				except:
					content_length += 0

		date_string = month + "/" + day + "/" + year

		date = datetime.datetime.strptime(date_string, format)

		if date not in history:
			history[date] = []
			history[date].append([title.replace("\\", ""), content_length])
		else:
			history[date].append([title.replace("\\", ""), content_length])

	return history