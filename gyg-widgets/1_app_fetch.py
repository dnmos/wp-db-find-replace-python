import requests
import json
from bs4 import BeautifulSoup
import re
from config import domen, category_slug, tpo_id_to_search, tpo_id_to_replace, trs_to_search, trs_to_replace

### Fetch post links ###
headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
}
count = 0
gygs = {}

def get_categories_from_api(headers):
	global category_slug
	if category_slug:
		# search category by slug
		uri = f"https://{domen}/wp-json/wp/v2/categories?search={category_slug}"
		request = requests.get(uri, headers=headers)
		category_json = json.loads(request.text)
		posts_in_category = str(category_json[0]['count'])
		posts_api = category_json[0]['_links']['wp:post_type'][0]['href'] + '&per_page=' + posts_in_category
		get_posts_from_api(posts_api)
	else:
		# search categories
		url = f"https://{domen}/wp-json/wp/v2/categories?per_page=50"
		request = requests.get(url, headers=headers)
		categories = json.loads(request.text)
		for category in categories:
			if category:
				posts_api = category['_links']['wp:post_type'][0]['href'] + '&per_page=' + str(category['count'])
				category_slug = category['slug']
				get_posts_from_api(posts_api=posts_api, headers=headers)

def get_posts_from_api(posts_api, headers):
	# for post in posts_api
	global category_slug, count
	request = requests.get(posts_api, headers=headers)
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
		result = soup.find_all('script', src=re.compile('c108'))
		for item in result:
			try:
				place = item['src'].split('place=')[1].split('&')[0]
				tour = ''
			except Exception as e:
				place = ''
				tour = item['src'].split('tour_id=')[1].split('&')[0]
				print(e)
			try:
				marker = item['src'].split('35039.')[1].split('&')[0]
			except Exception as e:
				marker = ''
				print(e)
			text_to_search = item['src'].replace('&', '&amp;')
			text_to_replace = f'//c108.travelpayouts.com/content?powered_by=false&locale=ru-RU&items=3&tour={tour}&place={place}&trs={trs_to_replace}&shmarker={tpo_id_to_replace}.{marker}&promo_id=4039'
			gygs[count] = {
				'category': category_slug, 
				'post_id': post_id, 
				'post_title': title,
				'post_slug': slug,
				'src': item['src'],
				'place': place,
				'marker': marker,
				'text_to_search': text_to_search,
				'text_to_replace': text_to_replace,
			}
			print(slug + ': ' + str(count))
			count += 1

	with open('./temp/result.json', 'w') as file:
		json.dump(gygs, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
	get_categories_from_api(headers=headers)