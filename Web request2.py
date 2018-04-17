import urllib3
import re
from bs4 import BeautifulSoup  # for parsing HTML
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

""" region httpRequest
http = urllib3.PoolManager()
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
           'Referer': 'https://www.mediamarkt.ru/item/1361208/apple-iphone-x-256gb-space-gray-smartfon',
           # 'cache-control': 'max-age=3600',
           # 'content-encoding': 'gzip',
           # 'content-type': 'text/css',
           # 'date': 'Thu, 12 Apr 2018 07:05:57 GMT',
           # 'etag': 'W/"5acda7ef-3570"',
           # 'expires': 'Thu, 12 Apr 2018 08:05:57 GMT',
           # 'last-modified': 'Wed, 11 Apr 2018 06:15:11 GMT',
           # 'server': 'nginx/1.12.2',
           # 'status': '304',
           # 'x-assets': '1'
           }
response = http.request('GET',
                        'https://www.mediamarkt.ru/item/1361208/apple-iphone-x-256gb-space-gray-smartfon#card-features',
                        headers=headers)

response = str(response.data, encoding='utf8')
endregion"""

response = open('jout_data.html', encoding='utf8', mode='r').readlines()
response = ''.join(response)

soup = BeautifulSoup(response, 'html.parser')

"""
characteristics = soup.find('div', {'class': 'characteristics__group additional'})

if characteristics:
    for li in characteristics.find_all('li'):
        # print(li.find_all("span"))
        if li.span is not None:
            a = str(li.find_all('span')[0])
            b = str(li.find_all('span')[1].string).strip()

            rex = re.compile(r"<mm-tooltip.*?>(?P<tooltip>.*?)</mm-tooltip>", re.DOTALL)
            result = rex.search(a)
            if result: print(f'tooltip: {result.group("tooltip")}')

            rex = re.compile(r"<span.+?>(?P<text>.+?)<", re.DOTALL)
            result = rex.search(a)
            if result: print(f"text: {result.group('text').strip()} :b: {b}")

        else:
            print('GROUP:', li.string)


description = soup.find('div', {"class": "reveal-block__content reveal-block__content--block"})
description = str(description.prettify())
description = re.sub(r"<div.*?>", '', description)
description = re.sub(r"</div>", '', description)
"""

for photo in soup.find_all('a',  {'class': "bullet"}):
    print(photo['data-ng-click'], end='\n\n\n')
# photos

