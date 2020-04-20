from bs4 import BeautifulSoup
import pandas as pd
import requests

# needs:
# pip install beautifulsoup4
# pip install requests 
# pip install pandas 

# referenced the following websites to create this code: 
# https://www.edureka.co/blog/web-scraping-with-python/
# https://medium.com/analytics-vidhya/web-scraping-html-table-from-wiki-9b18cf169359
# https://www.codementor.io/@dankhan/web-scrapping-using-python-and-beautifulsoup-o3hxadit4


url = "https://www.rapidtables.com/web/color/RGB_Color.html"

page = requests.get(url)

# should print 200 
# print(page.status_code)
# print(page.content)

soup = BeautifulSoup(page.content, "html.parser")


table = soup.findAll('table', class_="dtable")[2]

hex_codes =[]
decimal_codes =[]

inner_table = table.findAll('tr')

in_table = table.findAll('td')

for item in in_table:
	searchable_item = str(item)
	if searchable_item.startswith("<td>#"):
		searchable_item = searchable_item.replace("<td>#", "")
		searchable_item = searchable_item.replace("</td>", "")
		hex_codes.append(searchable_item)
	elif searchable_item.startswith("<td>("):
		searchable_item = searchable_item.replace("<td>", "")
		searchable_item = searchable_item.replace("</td>", "")
		decimal_codes.append(searchable_item)


df = pd.DataFrame({'RGB value': decimal_codes, 'Hex Code': hex_codes})

df.to_excel('RGB_Hex.xlsx', index = False)

print("Finished retrieving the RGB and Hex values. Saved as RGB_Hex.xlsx in project/app folder!")
















