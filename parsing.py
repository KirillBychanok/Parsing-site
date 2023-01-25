import json
import os.path
import urllib

import requests
from bs4 import BeautifulSoup

url = 'https://www.truckscout24.de/transporter/gebraucht/kuehl-iso-frischdienst/renault'

def get_data(url: str):
    headers = {
        'user-agent': 'Mozilla/5.0(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/108.0.0.0 Safari/537.36'
    }

    all_cars = []

    for item in range(1,5):
        req = requests.get(url + f'?currentpage={item}', headers)

        folder_name = f'data'

        if os.path.exists(folder_name):
            print('Папка существует')
        else:
            os.mkdir(folder_name)

        """
        Формирование базовой страницы
        """

        with open('index.html', 'w') as file:
            file.write(req.text)

        with open ('index.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        articles = soup.find('div', class_='ls-full-item')

        """
        Формирование URL каждого первого объявления
        """
        project_url = 'https://www.truckscout24.de' + articles.find('div', class_='ls-titles').find('a').get('href')
        

        req = requests.get(project_url, headers)
        car_name = project_url.split('/')[-2]

        folder_car_name = f'{folder_name}/{car_name}'

        if os.path.exists(folder_car_name):
            print('Папка существует')
        else:
            os.mkdir(folder_car_name)

        """
        Формирование HTML каждой страницы
        """

        with open(f'{folder_car_name}/first_ad_in_{item}_page.html', 'w') as file:
                file.write(req.text)

        with open(f'{folder_name}/{car_name}/first_ad_in_{item}_page.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        """
        Скачивание фото
        """

        links = soup.find_all('div', class_='gallery-picture')[0:3]
        for num, it in enumerate(links):
            photo = it.find('img', class_='gallery-picture__image sc-lazy-image lazyload').get('data-src')
            img = urllib.request.urlopen(photo).read()
            out = open(f'{folder_car_name}/{num}.jpg', "wb")
            out.write(img)
            out.close

        try:
            name = project_url.split('/')[-2]
        except Exception:
            name = 'Empty'
        try:
            href = project_url
        except Exception:
            href = 'Empty'
        try:
            title = soup.find('h1', class_='sc-ellipsis sc-font-xl').text
        except Exception:
            title = 'Empty'
        try:
            price = soup.find('div', class_='d-price sc-font-xl').text
        except Exception:
            price = 'Empty'
        try:
            miledge = soup.find('div', class_='data-basic1').find_all('div', class_='itemval')[1].text
        except Exception:
            miledge = 'Empty'
        try:
            colour = soup.find('div', class_='sc-expandable-box__content sc-grid-row').find('div', class_='sc-grid-col-12').find_all('li')[-6].find_all('div')[-1].text
        except Exception:
            colour = 'Empty'
        try:
            power = soup.find('div', class_='sc-expandable-box__content sc-grid-row').find('div', class_='sc-grid-col-12').find_all('li')[-3].find_all('div')[-1].text
        except Exception:
            power = 'Empty'
        try:
            description = soup.find_all('div', class_='sc-expandable-box__content')[-4].find('p').text
        except Exception:
            description = "Empty"

        all_cars.append(
                {
                'id': name,
                'href': href,
                'title': title,
                'price': price,
                'miledge': miledge,
                'colour': colour,
                'power': power,
                'description': description.strip().replace('\n', ' ')
                }
            )

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'{folder_car_name}/first_ad_in_{item}_page.html')
        os.remove(path)

    with open('data/projects_data.json', 'a', encoding='utf-8') as file:
        json.dump(all_cars, file, indent=4, ensure_ascii=False)

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'index.html')
    os.remove(path)


def main():
    get_data(url)


if __name__ == '__main__':
    main()