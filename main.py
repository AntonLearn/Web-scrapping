import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json


def get_headers():
    return Headers(browser='firefox', os='win').generate()


def parsed_site(url, params):
    parsed_data = []
    try:
        while True:
            hh_html = requests.get(url=url, params=params, headers=get_headers()).text
            hh_soup = BeautifulSoup(hh_html, 'lxml')
            print(f'Читаем страницу {params["page"]}')
            params['page'] += 1
            tag_content = hh_soup.find('div', id='a11y-main-content')
            div_item_tags = tag_content.find_all('div', class_='serp-item')
            for div_item_tag in div_item_tags:
                h3 = div_item_tag.find('h3')
                vacancy = h3.text
                link = h3.find('a').get('href')
                try:
                    salary = div_item_tag.find('span', class_='bloko-header-section-2').text.replace('\u202f', '')
                except:
                    salary = 'Не указана'
                company = div_item_tag.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', '')
                city = div_item_tag.find('div', class_='vacancy-serp-item__info').contents[1].contents[0]
                parsed_data.append({
                    "вакансия": vacancy,
                    "ссылка": link,
                    "зарплата": salary,
                    "название компании": company,
                    "город": city
                })
    except:
        print(f'Добавлено {len(parsed_data)} вакансий')
    return parsed_data


def write_json(site_data, filename, mode, encoding):
    with open(filename, mode, encoding=encoding) as file:
        json.dump(site_data, file, ensure_ascii=False, indent=5)


if __name__ == "__main__":
    FILENAME = 'vac.json'
    MODE = 'w'
    ENCODING = 'utf-8'
    URL = 'https://spb.hh.ru/search/vacancy'
    PARAMS = {
        'area': (1, 2),
        'text': 'python django flask',
        'page': 0,
        'items_on_page': 20
    }
    site_data = parsed_site(url=URL, params=PARAMS)
    if len(site_data)>0:
        write_json(site_data, filename=FILENAME, mode=MODE, encoding=ENCODING)