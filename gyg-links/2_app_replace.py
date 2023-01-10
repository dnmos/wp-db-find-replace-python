import pymysql
from config import domen, host, user, password, db_name, table, tpo_id_to_search, tpo_id_to_replace, trs_to_search, trs_to_replace 
import json

with open('/home/dm/app/data_analysis/gyg/temp/links.json') as file:
	links = json.load(file)

try:
	connection = pymysql.connect(
		host=host,
		port=3306,
		user=user,
		password=password,
		database=db_name,
		cursorclass=pymysql.cursors.DictCursor
	)
	print("Successfully connected...")
	print("#" * 20)

	try:
		cursor = connection.cursor()

		for link in links:
			post_id = link['post_id']
			text_to_search = link['link'].replace('&', '&amp;')
			text_to_replace_it_with = text_to_search.replace(tpo_id_to_search, tpo_id_to_replace).replace(trs_to_search, trs_to_replace)
			print(text_to_replace_it_with)

			with connection.cursor() as cursor:
				update_query = f"UPDATE `{table}` SET `post_content` =  \
												replace(\
													post_content,\
													'{text_to_search}',\
													'{text_to_replace_it_with}'\
												)\
												WHERE `{table}`.`ID` = {post_id};"
				cursor.execute(update_query)
				connection.commit()

	finally:
		connection.close()

except Exception as ex:
	print("Connection refused...")
	print(ex)