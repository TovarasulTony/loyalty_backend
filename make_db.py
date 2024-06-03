import os
import configparser
import randomname
import names
import random, string
from lorem_text import lorem
from flask_api import app, db
from flask_api.models import User, Manager, Brand
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

        delete_command = "rm /root/tony/loyalty_backend/site.db"
        os.system(delete_command)

        app.app_context().push()
        db.create_all()


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
        print(brand)
        db.session.add(brand)
        db.session.commit()


db_generator = DbGenerator()
db_generator.generate_brand()
