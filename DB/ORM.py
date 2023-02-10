from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from DB.model import Offer, Base
from settings import database_cinfig

engine = create_engine(database_cinfig.url, echo=False)
Session = sessionmaker(bind=engine)


def check_bd():
    engine = create_engine(database_cinfig.url)
    if not database_exists(engine.url):
        create_database(engine.url)
    print(f'База данных {database_cinfig.url.split("/")[-1]} созданна : {database_exists(engine.url)}')
    engine.dispose()


def clear():
    Base.metadata.drop_all(engine)
    engine.dispose()


def create_bd():
    check_bd()
    Base.metadata.create_all(engine)
    print('Таблицы созданы, база готова к работе \n')
    engine.dispose()


def add_offer(offer_hh):
    with Session() as session:
        offer = Offer(hh_id=int(offer_hh['id']),
                      name=offer_hh['name'],
                      salary=offer_hh['salary'],
                      employer=offer_hh['employer'],
                      metro=offer_hh['metro'],
                      skill=offer_hh['skill'],
                      work=offer_hh['work'],
                      date=offer_hh['date'],
                      link=offer_hh['link'],
                      )
        session.add(offer)
        session.commit()

    engine.dispose()


def recreate():
    clear()
    create_bd()


def get_offer(offer_hh):
    with Session() as session:
        offer = session.query(Offer).filter(Offer.hh_id == offer_hh['id']).first()
        engine.dispose()
        return offer


def inerest():
    with Session() as session:
        offer = session.query(Offer).filter(Offer.favorit == None).first()
        if not offer:
            print('Предложения кончились')
        engine.dispose()
        return offer


def sort_favorit():
    with Session() as session:
        offer = session.query(Offer).filter(Offer.favorit == 1).first()
        if not offer:
            print('Предложения кончились')
        engine.dispose()
        return offer


def add_favorit(offer_hh, fav):
    with Session() as session:
        offer = session.query(Offer).filter(Offer.hh_id == offer_hh).first()
        offer.favorit = fav
        session.add(offer)
        session.commit()
        engine.dispose()


def get_favorit():
    with Session() as session:
        offer = session.query(Offer).filter(Offer.favorit == 1).all()
        engine.dispose()
        return offer


def get_to_send():
    with Session() as session:
        offer = session.query(Offer).filter(Offer.favorit == 4).all()
        engine.dispose()
        return offer

# if __name__ == '__main__':
#     print(inerest())
