from pathlib import Path

import requests
from bs4 import BeautifulSoup

url_1 = 'https://codewithmosh.com/courses/enrolled/639884'
url_2 = 'https://codewithmosh.com/courses/enrolled/650827'
url_3 = 'https://codewithmosh.com/courses/enrolled/680168'

response = requests.get(url_3)

html = response.text

soup = BeautifulSoup(html, 'html.parser')

txt_path = Path() / 'resource' / 'TheUltimateDataStructures&Algorithms:Part3.txt'
txt_path.touch()

path = []

for link in soup.find_all('a'):
    url = link.get('href')
    if url is not None and url.startswith('/courses/'):
        download_url = 'https://' + 'codewithmosh.com' + url
        txt_path.write_text(download_url)
        path.append(download_url)

with open(txt_path, 'w') as file:
    for i in path:
        file.write(i + '\n')
