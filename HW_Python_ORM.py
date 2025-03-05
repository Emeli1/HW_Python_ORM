import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import os
from HW_models import create_tables, Publisher, Book, Shop, Stock, Sale

DNS = 'postgresql://postgres:postgres@localhost:5432/HW_Python_ORM'
engine = sqlalchemy.create_engine(DNS)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name='Пушкин')
book1 = Book(title='Капитанская дочка', publisher=publisher1)
book2 = Book(title='Руслан и Людмила', publisher=publisher1)
book3 = Book(title='Евгений Онегин', publisher=publisher1)
shop1 = Shop(name='Буквоед')
shop2 = Shop(name='Лабиринт')
shop3 = Shop(name='Книжный дом')
stock1 = Stock(book=book1, shop=shop1, count=60)
stock2 = Stock(book=book2, shop=shop1, count=50)
stock3 = Stock(book=book1, shop=shop2, count=58)
stock4 = Stock(book=book3, shop=shop3, count=49)
sale1 = Sale(price='600', date_sale='2022-11-09', stock=stock1, count='1')
sale2 = Sale(price='500', date_sale='2022-11-08', stock=stock2, count='1')
sale3 = Sale(price='580', date_sale='2022-11-05', stock=stock3, count='1')
sale4 = Sale(price='490', date_sale='2022-11-02', stock=stock4, count='1')
sale5 = Sale(price='600', date_sale='2022-10-26', stock=stock1, count='1')
session.add_all([publisher1, book1, book2, book3, shop1, shop2, shop3, stock1, stock2, stock3,
                 stock4, sale1, sale2, sale3, sale4, sale5])
session.commit()

# file_path = os.path.join(os.getcwd(), 'fixtures\\tests_data.json')
# with open(file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)
#     for item in data:
#         model = {
#             'publisher': Publisher,
#             'book': Book,
#             'shop': Shop,
#             'stock': Stock,
#             'sale': Sale
#         }[item.get('model')]
#         session.add(model(id=item.get('pk'), **item.get('fields')))
#     session.commit()

def get_sales(publisher):
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        select_from(Publisher).join(Book).join(Stock).join(Shop).join(Sale).order_by(Sale.date_sale.desc())
    if publisher.isdigit():
        query = query.filter(Publisher.id == publisher).all()
    else:
        query = query.filter(Publisher.name == publisher).all()

    for title, shop, price, date in query:
        print(f'{title} | {shop} | {price} | {date.strftime('%d-%m-%Y')}')


session.close()

if __name__ == '__main__':
    publisher = input('Введите имя или id издателя: ')
    get_sales(publisher)