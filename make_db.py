import os
import configparser
import randomname
import names
import random, string
from lorem_text import lorem
from flask_api import app, db
from flask_api.models import User, Manager, Brand, Card
from flask_api.enums import BRAND_TYPE
#from flask_test.random_generator import get_random_user, get_random_wallet

'''
# importing datetime module
import datetime
import time
 
# assigned regular string date
date_time = datetime.datetime(2021, 7, 26, 21, 20)
 
# print regular python date&time
print("date_time =>",date_time)
 
# displaying unix timestamp after conversion
unix_timestamp = time.mktime(date_time.timetuple())
print("unix_timestamp => ", unix_timestamp)
print(type(unix_timestamp))


exit()

app.app_context().push()
#db.create_all()

user=get_random_user()
print(user)
get_random_wallet()

'''
class DbGenerator():
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    brand_list = []

    def __init__(self):
        # IMPORTANT - the order of the files matters as they overriwte common variables
        self.config.read(['config/models.ini', 'config/generate_db.ini'])
        #app.app_context().push()

        delete_command = "rm /root/tony/loyalty_backend/site.db"
        os.system(delete_command)
        app.app_context().push()
        db.create_all()

        print('Generating Brands...')
        no_of_brands = int(self.config["brand"]["no_of_brands"])
        for i in range(0, no_of_brands):
            if i % (no_of_brands / 10) == 0:
                percentage = int((i / no_of_brands) * 100) + 10
                print(str(percentage) + '%')
            self.generate_brand()

        print('Generating Clients...')
        no_of_clients = int(self.config["brand"]["no_of_brands"]) * int(self.config["user"]["no_of_clients_multiplier"])
        for i in range(0, no_of_clients):
            if i % (no_of_clients / 10) == 0:
                percentage = int((i / no_of_clients) * 100) + 10
                print(str(percentage) + '%')
            user = self.generate_user()
            db.session.add(user)
        db.session.commit()

        print('Generating Cards...')
        all_clients = User.query.filter_by(manager=None)
        all_brands = Brand.query.all()
        i = 0
        #no_of_clients = all_clients.count()
        #no_of_brands = len(all_brands)
        for client in all_clients:
            i += 1
            if i % (no_of_clients / 10) == 0:
                percentage = int((i / no_of_clients) * 100)
                print(str(percentage) + '%')
            no_of_cards_per_client = random.randint(int(self.config["card"]["min_cards_per_user"]), int(self.config["card"]["max_cards_per_user"]))
            for j in range(0, no_of_cards_per_client):
                card = Card(
                    holder = client,
                    brand = all_brands[(i + j) % no_of_brands]
                )
                db.session.add(card)
        db.session.commit()

    def generate_user(self):
        user = User(
            nickname = names.get_full_name(),
            wallet_address = 'G' + ''.join([random.choice(string.ascii_uppercase  + string.digits) for _ in range(int(self.config["common"]["wallet_address_length"]))])
        )
        db.session.add(user)
        return user

    def generate_manager(self):
        manager = Manager(
            user = self.generate_user()
        )
        db.session.add(manager)
        return manager

    def generate_brand(self):
        brand = Brand(
            name = ''.join([x.title() for x in randomname.get_name().split('-')]),
            type = random.choice([x for x in BRAND_TYPE if x != BRAND_TYPE.Invalid]),
            program = lorem.sentence(),
            threshold = random.uniform(0, float(self.config["brand"]["threshold_max"])),

            manager = self.generate_manager()
        )
        db.session.add(brand)
        db.session.commit()


db_generator = DbGenerator()

