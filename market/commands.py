from market import app
from market import db
from market.models import Item, Users


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    phone = Item(name='Phone',
                 barcode='893212299897',
                 price='500',
                 description='1')

    laptop = Item(name='Laptop',
                  barcode='123985473165',
                  price='900',
                  description='2')

    keyboard = Item(name='Keyboard',
                    barcode='231985128446',
                    price='150',
                    description='3')

    test_user = Users(username='test',
                      email_address='test@test.com',
                      password_hash='testtest')

    deepak_user = Users(username='deepak',
                        email_address='deepak@singh.com',
                        password_hash='testtest')

    db.session.add_all([test_user, deepak_user, keyboard, laptop, phone])
    db.session.commit()

    print("Database Seeded!")