import requests
import json
from bs4 import BeautifulSoup
import re
from config import domen, category_name


### Fetch post links ###
headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
}

# search id of category_name
url = f"https://{domen}/wp-json/wp/v2/categories?per_page=50"
request = requests.get(url, headers=headers)
categories = json.loads(request.text)
print(category_name)
gygs = []
links_count = 0
for category in categories:
	if category_name and category['slug'] == category_name:
		posts_in_category = category['_links']['wp:post_type'][0]['href'] + '&per_page=' + str(category['count'])
	elif not category_name:
		posts_in_category = category['_links']['wp:post_type'][0]['href'] + '&per_page=' + str(category['count'])
	print(category['slug'])

	# for post in category_name
	request = requests.get(posts_in_category, headers=headers)
	posts = json.loads(request.text)
	for post in posts:
		url = post['_links']['self'][0]['href']
		request = requests.get(url, headers=headers)
		data = json.loads(request.text)
		post_id = data['id']
		title = data['title']['rendered']
		slug = data['slug']
		content = data['content']['rendered']
		soup = BeautifulSoup(content, 'lxml')
		links = soup.find_all('a', href=re.compile('getyourguide'))
		for link in links:
			links_count += 1
			gygs.append({
				'links_count': links_count,
				'category': category['slug'],
				'post_id': post_id,
				'post_title': title,
				'post_slug': slug,
				'link': link['href']
			})
			print(slug)

with open('/home/dm/app/data_analysis/gyg/temp/links.json', 'w') as file:
	json.dump(gygs, file, indent=4, ensure_ascii=False)
