import pymysql
from config import host, user, password, db_name, table 
import json

with open('./temp/result.json') as file:
	result = json.load(file)

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
	print("#" * 30)

	try:
		cursor = connection.cursor()

		for item in result:
			pass
			post_id = result[f'{item}']['post_id']
			text_to_search = result[f'{item}']['text_to_search']
			text_to_replace_it_with = result[f'{item}']['text_to_replace']
			print(text_to_replace_it_with)
			print(item)

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