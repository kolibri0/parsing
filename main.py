from time import sleep
import requests
from bs4 import BeautifulSoup
import os.path
import json
# url = r'http://hdstudio.org/novinki_serialy_1/page/2/'
# .encode('utf-8').decode('cp1251'))


def get_data(url, headers):
    serial_items_list_url = []
    serial_result_list = []
    check = os.path.exists('data/page_1.html')
    if not check:
        os.mkdir("data")
        r = requests.get(url=url, headers=headers)
        src = r.text
        with open('data/page_1.html', 'w', encoding='utf-16') as file:
            file.write(src)
        get_data(url=url, headers=headers)
    else:
        with open('data/page_1.html', encoding='utf-16', errors='ignore') as file:
            src = file.read()
            soup = BeautifulSoup(src, "lxml")
            pages_count = int(soup.find(
                'div', class_='navigation').find_all('a')[-2].text)
        for page in range(1, pages_count + 1):
            if page != 1:
                url = f'http://hdstudio.org/novinki_serialy_1/page/{page}/'
            res = requests.get(url=url, headers=headers)
            with open(f'data/page_{page}.html', 'w', encoding='utf-16') as file:
                file.write(res.text)
            print(f'page : {page}')
            sleep(3)

            with open(f'data/page_{page}.html', encoding='utf-16', errors='ignore') as file:
                src = file.read()
                soup = BeautifulSoup(src, "lxml")
                items_list_a = soup.find(
                    'div', 'items-box').find_all('a')
                for item_a in items_list_a:
                    item_url = item_a['href']
                    serial_items_list_url.append(item_url)
    if len(serial_items_list_url):
        for serial_item_url in serial_items_list_url:
            # for serial_item_url in serial_items_list_url[1:2]:
            r = requests.get(url=serial_item_url, headers=headers)
            src = r.content.decode(encoding='cp1251', errors='ignore')
            soup = BeautifulSoup(src, "lxml")
            item_title = soup.find('h1', class_='head-title').find('span').text
            item_img = f'http://hdstudio.org' + \
                soup.find('a', class_='highslide').find('img')['src']
            item_rating = soup.find('div', class_='reliz_rating_in').find(
                'b').find('span').text + '/5'
            item_description = soup.find(
                'article', class_='eText').text.strip()
            serial_result_list.append(
                {
                    'img_url': item_img,
                    'name': item_title,
                    'rating': item_rating,
                    'description': item_description
                }
            )
            print(f'{item_title} is ready')
            sleep(2)
    with open('result_serial.json', 'w') as file:
        json.dump(serial_result_list, file, indent=4, ensure_ascii=False)


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    url = r'http://hdstudio.org/novinki_serialy_1'
    get_data(url=url, headers=headers)


if __name__ == '__main__':
    main()
