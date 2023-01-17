from time import sleep

from DB import ORM
from hh import sercher_hh



if __name__ == '__main__':
    # ORM.recreate()


    '''Заполнение базы '''
    for offer_hh in sercher_hh.get_id_offer(8):
        if ORM.get_offer(offer_hh):
            continue
        else: ORM.add_offer(offer_hh)

    while True:
        offer = ORM.inerest()

        if offer:
            print(offer)
            ans = input('\n Куда добавить : 1 - избранное, 2 - не показывать \n')
            if ans in  ['2', '1']:

                ORM.add_favorit(offer.hh_id,int(ans))
        else: break

    sleep(1)
    fav = input('Показать избранное ?  (да / что то )')
    if fav.lower() == 'да':
        for ofer in ORM.get_favorit():
            print(ofer)
            print()
            print('*' * 50)
            print()
