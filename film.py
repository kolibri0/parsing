from time import sleep
import requests
from bs4 import BeautifulSoup
import os.path
import re
import json
# url = r'http://hdstudio.org/novinki_serialy_1/page/2/'
# .encode('utf-8').decode('cp1251'))

# >>> os.path.join('home', 'User', 'Desktop', 'file.txt')
# 'home/User/Desktop/file.txt'

start_path = 'https://ru.kinorium.com'
folder_path = 'data'


def get_data(url, headers):
    print(url)
    film_result_list = []
    film_name = url.split("q=")[1]
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')

    films = soup.find('div', class_='list movieList').find_all(
        'div', class_='item')

    # ------------------------------------For Films------------------------------------
    for film in films:

        link = film.find('h3', class_='search-page__item-title link-info-movie').find(
            'a', class_='search-page__title-link search-page__item-title-text').get('href')
        link = start_path + link
        res = requests.get(url=link, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        # ---------------------------------------Name---------------------------------------

        film_name = soup.find(
            'h1', class_='film-page__title-text film-page__itemprop').text

        # --------------------------------------Year----------------------------------------

        year = soup.find('span', class_='data film-page__date').find('a').text

        # --------------------------------------Countryes--------------------------------------

        countrys = []
        countrys_soup = soup.find_all('a', class_='film-page__country-link')
        for country in countrys_soup:
            if not country:
                return
            countrys.append(country.text)

        # --------------------------------------Description----------------------------------

        film_description = soup.find(
            'section', itemprop='description').text

        # --------------------------------------Genres-----------------------------------------

        film_genres = []
        film_genres_soup = soup.find('ul', class_='film-page__genres genres').find_all(
            'li',                                                                 itemprop='genre')
        for film_genre_soup in film_genres_soup:
            film_genres.append(film_genre_soup.text)

        # ------------------------------------Add To Result List--------------------------------

        film_result_list.append(
            {
                'name': film_name,
                'year': year,
                'country': countrys,
                'genres': film_genres,
                'description': film_description
            }
        )

    # ---------------------------------------RESULT-------------------------------------------
    with open(f'data/{film_name}.json', 'w', encoding='utf-16') as file:
        json.dump(film_result_list, file, indent=4, ensure_ascii=False)


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    film_name = input('Enter film name: ')
    url = fr'https://ru.kinorium.com/search/?q={film_name}'
    get_data(url=url, headers=headers)


if __name__ == '__main__':
    main()
