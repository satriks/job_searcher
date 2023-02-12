import asyncio
from datetime import date
from time import sleep

import pandas as pd
from tqdm import tqdm

from DB import ORM
from hh.sercher_hh_asynco import loop
from hh import sercher_hh

SEARCH = ['python', 'python стажер', 'python junior', 'python fullstack', 'python разработчик']


def to_exel():
    '''вывод избранного в эксель'''
    data = pd.DataFrame(
        [(x.name, x.salary, x.employer, x.metro, x.skill, x.work, x.date, x.link, x.favorit, x.hh_id) for x in
         ORM.get_favorit()])
    data.to_excel("output.xlsx",
                  header=['Название', 'Зарплата', 'Кто', 'Метро', 'Знания', 'Что делать', 'Дата', 'Ссылка', 'favorit',
                          'hh_id'])


def to_exel_to_send():
    '''вывод  вакансий для отправки резюме'''
    data = pd.DataFrame(
        [(x.name, x.salary, x.employer, x.metro, x.skill, x.work, x.date, x.link, x.favorit, x.hh_id) for x in
         ORM.get_to_send()])
    data.to_excel(f"to_send_{date.today()}.xlsx",
                  header=['Название', 'Зарплата', 'Кто', 'Метро', 'Знания', 'Что делать', 'Дата', 'Ссылка', 'favorit',
                          'hh_id'])


def to_terminal():
    '''Показать избранное '''
    data = ORM.get_favorit()
    print('-' * 30)
    for ofer in data:
        print(ofer)
        print()
        print('*' * 50)
        print()
    print(f'Всего в избранном : {len(data)}')


# ORM.recreate()


def serch_offer(srch, offer_count):
    '''Поиск предложений '''
    for request_hh in tqdm(srch, colour='BLUE', ncols=80, desc='Идет поиск вакансий '):
        for offer_hh in sercher_hh.get_id_offer(offer_count, text=request_hh):
            if ORM.get_offer(offer_hh):
                continue
            else:
                ORM.add_offer(offer_hh)
    print()


def sorted_offer():
    '''сортировка предложений'''
    while True:
        offer = ORM.inerest()
        if offer:
            print(offer)
            ans = input('\n Куда добавить : 1 - избранное, 2 - не показывать \n')
            if ans in ['2', '1']:
                ORM.add_favorit(offer.hh_id, int(ans))
        else:
            break


def sorted_favorit():
    while True:
        offer = ORM.sort_favorit()
        if offer:
            print(offer)
            ans = input('\n Будем отправлять ?  3/нет 4/да \n')
            if ans in ['3', '4']:
                ORM.add_favorit(offer.hh_id, int(ans))
        else:
            break


def info():
    fav = input('Показать избранное ?  (1 - терминал / 2 - эксель / продолжить - anykey ) \n')
    if fav == '1':
        to_terminal()
    elif fav == '2':
        to_exel()


def start(deep=10, srch=SEARCH):

    # serch_offer(srch, deep)
    asyncio.run(loop(SEARCH, deep))
    sorted_offer()
    sleep(1)
    print()
    info()


if __name__ == '__main__':
    # ORM.check_bd()
    start(50)
    # sorted_favorit()
    # to_exel_to_send()
