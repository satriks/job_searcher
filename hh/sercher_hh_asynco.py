import asyncio, aiohttp
import json

from tqdm.asyncio import tqdm
from fake_headers import Headers

from DB import ORM

# SEARCH = ['python', 'python стажер', 'python junior', 'python fullstack', 'python разработчик']

def get_headers():
    return Headers(browser='firefox', os='win').generate()

async def get_offer(url, session, params):
     async with session.get(url, params=params, headers=get_headers()) as response:
        req = (await response.text())
        offers = prepare_data(req)
        for offer_hh in tqdm(offers, desc='Запись результатов', colour='green'):
            if ORM.get_offer(offer_hh):
                continue
            else:
                ORM.add_offer(offer_hh)


def prepare_data(req):
    data_list = []
    data = json.loads(req)
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


async def loop( searc_list, deep=10):
    tasks = []
    url = 'https://api.hh.ru/vacancies'
    params = {'text': 'python junior', 'area': (1), 'period': 30, 'experience': 'noExperience', 'per_page': 2,
              'order_by': 'publication_time'}
    SEARCH = searc_list
    async with aiohttp.ClientSession() as session:
        for text in tqdm(SEARCH, desc='Запросы', colour='BLUE'):
            params['text'] = text
            params['per_page'] = deep
            task = asyncio.create_task(get_offer(url, session, params))
            tasks.append(task)
        await asyncio.wait(tasks)

# if __name__ == '__main__':
#     asyncio.run(loop())