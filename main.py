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
for i in range(0, 96, 24):
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
results = []
count = 0
for url in href_list:
    count +=1
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    info_block = soup.find('div', class_='top-info-cont')
    name_of_fest = info_block.find('h1').text.strip()
    date_of_fest = info_block.find('h3').text.strip()
    location_url ='https://www.skiddle.com' + info_block.find('a').get('href')

    # получение данных о локации
    req = requests.get(url=location_url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    contact_details = soup.find('h2', string='Venue contact details and info').find_next()
    items = [item.text for item in contact_details.find_all('p')]

    contact_detail_dict = {}
    for i in items:
        contact_detail_list = i.split(':')
        if len(contact_detail_list) == 3:
            contact_detail_dict[contact_detail_list[0].strip()] = contact_detail_list[1].strip() + ':'\
                                                                    + contact_detail_list[2].strip()
        else:
            contact_detail_dict[contact_detail_list[0].strip()] = contact_detail_list[1]
    results.append({
        'Name': name_of_fest,
        'Date': date_of_fest,
        'Contact date': contact_detail_dict
    })
    print(count)

with open('result.json', 'a', encoding='utf-8') as file:
    json.dump(results, file, indent=4,ensure_ascii=False)