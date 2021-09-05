import requests
from bs4 import BeautifulSoup
import lxml
import json


headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

href_list = []

# сбор ссылок
for i in range(0, 24, 24):
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=24%20Jan%202021&to_date=&where%5B%5D=2&where%5B%5D=3&where%5B%5D=4&where%5B%5D=6&where%5B%5D=7&where%5B%5D=8&where%5B%5D=9&where%5B%5D=10&maxprice=500&o={i}&bannertitle=May"
    req = requests.get(url=url, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data['html']

    with open(f'index_{i}.html', 'w', encoding='utf-8') as file:
        file.write(html_response)

    with open(f'index_{i}.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    cards = soup.find_all('a', class_='card-img-link')
    for item in cards:
        href = item.get('href')
        href_list.append('https://www.skiddle.com' + href)

# сбор информации из ссылок
for url in href_list:
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    info_block = soup.find('div', class_='top-info-cont')
    name_of_fest = info_block.find('h1').text.strip()
    date_of_fest = info_block.find('h3').text.strip()
    location_url ='https://www.skiddle.com' + info_block.find('a').get('href')

    # получение данных о локации
    req = requests.get(url=location_url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')