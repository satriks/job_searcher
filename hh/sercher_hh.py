import json
import time

import aiohttp
import asyncio
import requests
from fake_headers import Headers

HOST = 'https://api.hh.ru/vacancies'
params = {'text': 'python junior', 'area': (1), 'period': 30, 'experience': 'noExperience', 'per_page': 2,
          'order_by': 'publication_time'}


def get_headers():
    return Headers(browser='firefox', os='win').generate()


async def get_asinc_offer(per_page=10, text='python junior'):
    data_list = []
    params['per_page'] = per_page
    params['text'] = text
    async with aiohttp.ClientSession() as sesion:
        return sesion.get(HOST, headers=get_headers(), params=params)


def get_id_offer(per_page=10, text='python junior'):
    data_list = []
    params['per_page'] = per_page
    params['text'] = text
    req = requests.get(HOST, headers=get_headers(), params=params)
    data = json.loads(req.text)
    # print(data)
    for offer in data['items']:

        if offer['salary']:
            selary = f"{offer['salary']['from']} - {offer['salary']['to']} {offer['salary']['currency']}"
        else:
            selary = 'Не указана'

        if offer['address']:
            metro = offer['address']['metro_stations']
            if metro:
                metro = metro[0]['station_name']
            else:
                metro = 'Не указано'
        else:
            metro = 'Не указано'

        if offer['snippet']['responsibility']:
            work = offer['snippet']['responsibility'].replace('<highlighttext>', '').replace('</highlighttext>', '')
        else:
            work = offer['snippet']['responsibility']

        if offer['snippet']['requirement']:
            skill = offer['snippet']['requirement'].replace('<highlighttext>', '').replace('</highlighttext>', '')
        else:
            skill = offer['snippet']['responsibility']

        data_list.append({
            'name': offer['name'],
            'link': (offer['alternate_url']),
            'salary': selary,
            'employer': (offer['employer']['name']),
            'metro': metro,
            'skill': skill,
            'work': work,
            'date': offer['published_at'].split('T')[0],
            'id': offer['id'],
        })

    # return sorted(data_list, key=lambda x : x['date'], reverse=True)  Вместо этого упорядочил поиск по дате в param
    return data_list


if __name__ == '__main__':
    timestart = time.time()
    test = get_id_offer()
    print(time.time() - timestart)
    # print(*get_id_offer(), sep='\n \n')
    timestart2 = time.time()
    ofers = asyncio.run(get_asinc_offer())
    print(time.time() - timestart2)
    print(test == ofers)
