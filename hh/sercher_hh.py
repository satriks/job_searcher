import json

import requests

from fake_headers import Headers

HOST = 'https://api.hh.ru/vacancies'
params ={'text': 'python junior', 'area': (1), 'period': 30, 'experience' : 'noExperience' , 'per_page':2, 'order_by': 'publication_time'}

def get_headers():
    return Headers(browser='firefox', os='win').generate()



def get_id_offer(per_page=10):
    data_list = []
    params['per_page'] = per_page
    req = requests.get(HOST,headers=get_headers(), params=params)
    data = json.loads(req.text)
    for d in data['items']:

        if d['salary']:
            selary = f"{d['salary']['from']} - {d['salary']['to']} {d['salary']['currency']}"
        else: selary = 'Не указана'

        if d['address']:
            metro = d['address']['metro_stations']
            if metro:
                metro = metro[0]['station_name']
            else:
                metro = 'Не указано'
        else:
            metro = 'Не указано'
        data_list.append({
            'name' : d['name'],
            'link': (d['alternate_url']),
            'salary': selary,
            'employer': (d['employer']['name']),
            'metro': metro,
            'skill' : d['snippet']['requirement'].replace('<highlighttext>', '').replace('</highlighttext>',''),
            'work' : d['snippet']['responsibility'],
            'date': d['published_at'].split('T')[0],
            'id': d['id'],

        })

    # return sorted(data_list, key=lambda x : x['date'], reverse=True)  Вместо этого упорядочил поиск по дате в param
    return data_list



if __name__ == '__main__':
    print(*get_id_offer(), sep='\n \n')