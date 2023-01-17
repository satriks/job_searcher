from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Offer(Base):
    __tablename__ = 'offer'
    offer_id = Column(Integer, primary_key=True, index=True)
    hh_id = Column(Integer, nullable=False, index=True)
    name = Column(String)
    salary = Column(String)
    employer = Column(String)
    metro = Column(String)
    skill = Column(String)
    work = Column(String)
    date = Column(String)
    link = Column(String)
    favorit = Column(Integer)

    def __repr__(self):
        return f' Название : {self.name} \n' \
               f' Зарплата : {self.salary} \n' \
               f' Кто :  {self.employer} \n' \
               f' Метро :  {self.metro}  \n' \
               f' Знания : {self.skill} \n' \
               f' Что делать : {self.work} \n' \
               f' Дата : {self.date} \n' \
               f' Ссылка : {self.link} \n' \
               f' Просмотренно :  {self.favorit}'
