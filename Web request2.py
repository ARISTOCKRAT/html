import urllib3
import re
from bs4 import BeautifulSoup  # for parsing HTML
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

out_dict = dict()
out_dict['properties'] = []

# region httpRequest
http = urllib3.PoolManager()
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
           'Referer': 'https://www.mediamarkt.ru/item/1361208/apple-iphone-x-256gb-space-gray-smartfon',
           }
response = http.request('GET',
                        'https://www.mediamarkt.ru/item/1361208/apple-iphone-x-256gb-space-gray-smartfon#card-features',
                        headers=headers)

response = str(response.data, encoding='utf8')
# endregion

# response = open('jout_data2.html', encoding='utf8', mode='r').readlines()
# response = ''.join(response)
with open('out_data2.html', encoding='utf8', mode='w') as f:
    f.write(response)
    f.close()

soup = BeautifulSoup(response, 'html.parser')

# Getting CHARACTERISTICS of product
characteristics = soup.find('div', {'class': 'characteristics__group additional'})
if characteristics:
    for li in characteristics.find_all('li'):
        # print(li.find_all("span"))
        if li.span is not None:
            a = str(li.find_all('span')[0])
            b = str(li.find_all('span')[1].string).strip()

            rex = re.compile(r"<span.+?>(?P<text>.+?)<", re.DOTALL)
            result = rex.search(a)
            if result:
                print(f"text: {result.group('text').strip()} :b: {b}")
                out_dict['characteristics'].append([result.group('text').strip(), b])

            rex = re.compile(r"<mm-tooltip.*?>(?P<tooltip>.*?)</mm-tooltip>", re.DOTALL)
            result = rex.search(a)
            if result:
                print(f'tooltip: {result.group("tooltip")}')
                out_dict['characteristics'][-1].append(result.group('tooltip'))

        else:
            print('GROUP:', li.string)
            out_dict['characteristics'].append(li.string)

# Getting DESCRIPTION
description = soup.find('div', {"class": "reveal-block__content reveal-block__content--block"})
description = str(description.prettify())
description = re.sub(r"<div.*?>", '', description)
description = re.sub(r"</div>", '', description)
out_dict['description'] = description
print(out_dict['description'])

# Getting IMAGE LINKS
out_dict['img_link'] = []
for photo in soup.find_all('a',  {'class': "bullet"}):
    if photo.get('data-ng-click'):
        rex = re.compile(r".*showBigImage.*?event,.*?\'(?P<img_link>http.*?)\'.*?bullet=(?P<num>[0-9]+)", re.DOTALL)
        result = rex.search(photo['data-ng-click'])
        if result:
            print(f"img_link: {result.group('img_link').strip()}; Bullet={result.group('num')}")
            out_dict['img_link'].append([result.group('img_link').strip(),
                                         result.group('num')])
# photos

# Getting IDENTIFICATION number
id_number = soup.find('div', {'class': 'card__article'}).div['id']
print(f"АРТИКУЛ: {id_number}")
out_dict['id_number'] = id_number

# Getting IMAGE from LINKS
for link in out_dict['img_link']:
    response = http.request('GET', link[0], headers=headers, preload_content=False)
    path = r"c:\Users\LocalAdmin\_JuPyteR\data\\" \
           f"{id_number}-{out_dict['img_link'][1]}"
    with open(path, 'wb') as out:
        while True:
            data = response.read(1024)
            if not data:
                break
            out.write(data)
    response.release_conn()

