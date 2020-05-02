from pathlib import Path
import requests
from bs4 import BeautifulSoup
import time
from util.get_cookies import get_cookies
from util.segment import multiThreadDownload
from util.send_email import send_email


cookies = get_cookies()
headers = {'Cookie': cookies}
homepage = 'https://codewithmosh.com/courses/enrolled/240431'
response_home = requests.get(homepage, headers=headers)
soup_home = BeautifulSoup(response_home.text, 'html.parser')

course_dict = {}

for i in soup_home.find_all('div', {'class': 'row'}):
    course_name = i.find('div', {'class': 'course-listing-title'}).string
    course_name = course_name.split('\n')[1].split('\n')[0].split('(')[0].strip()
    course_url = i.find('a').get('href')
    course_url = 'https://' + 'codewithmosh.com' + course_url
    course_dict.update({course_name: course_url})

print('Available courses')
print(20 * '*')
course_no_dict = {}
for num, key in enumerate(course_dict):
    print(f'{num}: {key}')
    course_no_dict.update({num: key})
print(20 * '*')

course_no = int(input('Choose a course by number: '))
assert course_no in range(len(course_dict))

course_title = course_no_dict[course_no]
print(f'"{course_title}" is chosen')
print('Gathering download information...')
print()

# ****************
url = course_dict[course_no_dict[course_no]]

# http get
response = requests.get(url, headers=headers)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

info_dic = {}

for num, section in enumerate(soup.find_all('div', {'class': 'col-sm-12 course-section'})):
    sectionTitle = section.find('div', {'class': 'section-title'})
    section_name = list(sectionTitle.strings)[3].split('\n')[1].split('\n')[0].split('(')[0].strip()
    section_name = str(num + 1) + '- ' + section_name
    section_info_list = []

    print(f'Section: {section_name}')

    for lectureUrl in section.find_all('a'):
        url = 'https://' + 'codewithmosh.com' + lectureUrl.get('href')
        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        for link in soup.find_all('a', {'class': 'download'}):
            file_url = link.get('href')
            header = requests.head(file_url).headers
            file_size = int(header["Content-Length"])
            file_name = header["X-File-Name"]
            print(file_name, f'{(file_size / 1000000):.2f}mb', file_url)
            section_info_list.append({"file_name": file_name, "file_size": file_size, "file_url": file_url})

    info_dic.update({section_name: section_info_list})

print('Gathering information complete')
print(20 * '*')

# make dir
print('Creating folder')
if not (Path() / 'resource').exists():
    (Path() / 'resource').mkdir()

course_path = Path() / 'resource' / course_title
if not course_path.exists():
    course_path.mkdir()

for section in info_dic.keys():
    dir_path = course_path / section
    if not dir_path.exists():
        dir_path.mkdir()
print('Creating folder complete')
print(20 * '*')

print('Start downloading...')
print()

startTime = time.time()

for section in info_dic.keys():
    for file_info in info_dic[section]:
        download_link = file_info['file_url']
        download_name = file_info['file_name']
        download_size = file_info['file_size']

        print(f'Downloading: {download_name}')
        print(f'From url: {download_link}')
        print(f'File size: {download_size / 1_000_000} mb')

        path = Path() / 'resource' / course_title / section / download_name

        start_time = time.time()
        thread_num = 10

        multiThreadDownload(url=download_link, file_path=path, file_size=download_size, thread_num=thread_num)

        finish_time = time.time()
        time_download = finish_time - start_time
        speed = float(download_size) / (1000000.0 * time_download)
        print('Download complete!')
        print(f'Download time: {time_download:.2f}s')
        print(f'Download speed: {speed:.2f}mb/s')
        print(10 * '*')

endTime = time.time()
total_time = endTime - startTime
print('all finished!')
print(f'total time: {total_time:.0f}s')


message = f'{course_title} download complete! Total time: {total_time:.2f}s'
send_email(message)
