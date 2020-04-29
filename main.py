import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from util.segment import multiThreadDownload

txt_path = Path() / 'resource' / 'data_structure' / 'download_link' / 'TheUltimateDataStructures&Algorithms:Part1.txt'
url_list = []
with open(txt_path) as fp:
    for line in fp:
        url_list.append(line.split('\n')[0])

startTime = time.time()

for url in url_list:

    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
        # 'Host': 'codewithmosh.com',
        'Cookie': '_ga=GA1.2.1389156800.1586815101; _gid=GA1.2.348802966.1587774863; ajs_group_id=null; ajs_user_id=30796709; ac_enable_tracking=1; _session_id=ba4a4da3e6b0bbd8a2300332d01be90d; ahoy_visit=76e3c1e0-0909-40be-8f67-edc004be8e9c; signed_in=true; site_preview=logged_in; wistiaVisitorKey=b433d64_3a16f34c-36b6-442c-81ec-c7ebdebbc8f2-10ce11ac0-bab5f04a548b-c7ab; __cfruid=d9f2638715dfbad6424fd01503c4f96b42da8c82-1587774861; ajs_anonymous_id=%22e8defab2-5124-4aff-bf08-421c494e8ec0%22; __cfduid=d676dd83c00058dc896df854a836162e81572048804; _afid=6ec53aa8-63f9-407b-b7c8-e2f160ea8b09; aid=6ec53aa8-63f9-407b-b7c8-e2f160ea8b09; ahoy_visitor=6ec53aa8-63f9-407b-b7c8-e2f160ea8b09',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('a', {'class': 'download'}):
        download_link = link.get('href')
        header = requests.head(download_link).headers

        file_name = header["X-File-Name"]
        file_size = int(header["Content-Length"])

        print(f'Downloading: {file_name}')
        print(f'From url: {download_link}')
        print(f'File size: {file_size / 1_000_000} mb')
        path = Path() / 'resource' / 'data_structure' / 'data_structure_1' / file_name
        path.exists()

        start_time = time.time()
        thread_num = 10

        multiThreadDownload(url=download_link, file_path=path, file_size=file_size, thread_num=thread_num)

        finish_time = time.time()
        time_download = finish_time - start_time
        speed = float(file_size) / (1000000.0 * time_download)
        print('Download complete!')
        print(f'Download time: {time_download}')
        print(f'Download speed: {speed}mb/s')
        print(20 * '-')

endTime = time.time()
time = endTime - startTime
print('all finished!')
print(f'total time:{time}')
