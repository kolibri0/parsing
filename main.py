from time import sleep
import requests
from bs4 import BeautifulSoup
import os.path
# url = r'http://hdstudio.org/novinki_serialy_1/page/2/'
# .encode('utf-8').decode('cp1251'))


def get_data(url, headers):

    check = os.path.exists('data/page_1.html')
    if not check:
        r = requests.get(url=url, headers=headers)
        src = r.text
        with open('data/page_1.html', 'w', encoding='utf-16') as file:
            file.write(src)
        get_data(url=url, headers=headers)
    else:
        # print('file asdadasd')
        with open('data/page_1.html', encoding='utf-16', errors='ignore') as file:
            src = file.read()
            soup = BeautifulSoup(src, "lxml")

    # print(check)
    # pass


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    url = r'http://hdstudio.org/novinki_serialy_1'
    get_data(url=url, headers=headers)


if __name__ == '__main__':
    main()
