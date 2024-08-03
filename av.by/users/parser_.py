import requests
import sqlalchemy
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = sqlalchemy.orm.declarative_base()


class Avto(Base):
    __tablename__ = "avto"
    id = Column(Integer, primary_key=True)
    brand = Column(String)
    price = Column(Integer)
    description = Column(String)


class Parser:
    links_to_parse = [
        'https://auto.kufar.by/?elementType=popular_categories',
        'https://auto.kufar.by/l/cars?elementType=auto_mp'
    ]

    def __init__(self):
        self.engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_avto_by_link(self, link):
        response = requests.get(link)
        with open("parser.html", "r", encoding="utf-8") as file:
            avto_data = file.read()

        avto_items = []
        to_parse = BeautifulSoup(avto_data, 'html.parser')
        for elem in to_parse.find_all('a', class_='styles_wrapper__yaLfq'):
            try:
                price, description = elem.text.split('р.')
                avto = Avto(brand=elem.text, price=int(price.replace(' ', '')), description=description)
                avto_items.append(avto)
            except Exception as e:
                print(f'Ошибка при парсинге элемента: {elem.text}. Подробности: {e}')

        return avto_items

    def save_to_postgres(self, avto_items):
        for avto in avto_items:
            self.session.add(avto)
        self.session.commit()

    def run(self):
        avto_items = []
        for link in self.links_to_parse:
            avto_items.extend(self.get_avto_by_link(link))
        self.save_to_postgres(avto_items)


if __name__ == "__main__":
    parser = Parser()
    parser.run()
