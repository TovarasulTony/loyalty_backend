import abc
from sqlalchemy import Enum
from flask_api import db, config
from flask_api.enums import USER_TYPE, BRAND_TYPE, TRANSACTION_TYPE


class Log():
    def __init__(self, title, number_of_spaces):
        self.number_of_spaces = number_of_spaces
        self.special_character = " "
        self.prefix = (number_of_spaces * 5)* self.special_character + '* '
        self.return_string = self.prefix + '{ ' + title + ' }' + '\n'
        self.return_string += self.prefix + '---------\n'

    def formated_log(self):
        return self.return_string

    def add_field(self, field_name, value):
        self.return_string += self.prefix + f'[{field_name}]: {value}\n'

    def add_relation(self, field_name, relation_list):
        self.return_string += self.prefix + f'[{field_name}]:\n'
        for object in relation_list:
            self.return_string += object.log(self.number_of_spaces + 1)

    def add_backref(self, field_name, backref):
        self.return_string += backref.log(self.number_of_spaces + 1)

class Logger():
    def log(self, number_of_spaces = 0):
        message = "[ERROR] Functie neimplementata"
        print(message)
        return message

class User(db.Model, Logger):
    #[Keys and Foreign Keys]
    id = db.Column(db.Integer, primary_key=True)

    #[Fields]
    nickname = db.Column(db.String(int(config["user"]["nickname_length"])), nullable=False)
    wallet_address = db.Column(db.String(int(config["user"]["wallet_address_length"])), nullable=False)

    #[Relationships]
    cashier = db.relationship('Cashier', backref='user', lazy=True)
    manager = db.relationship('Manager', backref='user', lazy=True)
    cards = db.relationship('Card', backref='holder', lazy=True)
    transactions = db.relationship('Transaction', backref='sender', lazy=True)

    def log(self, number_of_spaces=0):
        log = Log("User" , number_of_spaces)
        log.add_field('ID', self.id)
        log.add_field('Nickname', self.nickname)
        log.add_field('Wallet Address', self.wallet_address)
        if self.manager:
            log.add_relation('Manager', self.manager)
        if self.cashier:
            log.add_relation('Cashier', self.cashier)
        return log.formated_log()

class Cashier(db.Model, Logger):
    #[Keys and Foreign Keys]
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))

    #[Fields]
    #N/A

    #[Relationships]
    transactions = db.relationship('Transaction', backref='initiator', lazy=True)

    def log(self, number_of_spaces=0):
        log = Log("Cashier" , number_of_spaces)
        log.add_field('ID', self.id)
        if self.shop:
            log.add_backref('Shop', self.shop)
        return log.formated_log()

class Manager(db.Model, Logger):
    #[Keys and Foreign Keys]
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #[Fields]
    #N/A

    #[Relationships]
    #user = db.relationship('User', backref='manager', lazy=True)
    brand = db.relationship('Brand', backref='manager', lazy=True)
    #transactions = db.relationship('Transaction', backref='initiator', lazy=True)

    def log(self, number_of_spaces=0):
        log = Log("Manager" , number_of_spaces)
        log.add_field('ID', self.id)
        return log.formated_log()

class Card(db.Model, Logger):
    #[Keys and Foreign Keys]
    id = db.Column(db.Integer, primary_key=True)
    holder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)

    #[Fields]
    #N/A

    #[Relationships]
    transactions = db.relationship('Transaction', backref='card', lazy=True)

    def log(self, number_of_spaces=0):
        log = Log("Card" , number_of_spaces)
        log.add_field('ID', self.id)
        log.add_backref('Holder', self.holder)
        log.add_backref('Brand', self.brand)
        return log.formated_log()

class Brand(db.Model, Logger):
    #[Keys and Foreign Keys]
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)

    #[Fields]
    name = db.Column(db.String(int(config["brand"]["name_length"])), nullable=False)
    type = db.Column(Enum(BRAND_TYPE), nullable=False)
    program = db.Column(db.String(int(config["brand"]["program_length"])), nullable=False)
    threshold = db.Column(db.Double, nullable=False)

    #[Relationships]
    #manager = db.relationship('Manager', backref='brand', lazy=True)
    shops = db.relationship('Shop', backref='brand', lazy=True)
    cards = db.relationship('Card', backref='brand', lazy=True)

    def log(self, number_of_spaces=0):
        log = Log("Brand" , number_of_spaces)
        log.add_field('ID', self.id)
        log.add_field('Name', self.name)
        log.add_field('Type', self.type)
        log.add_field('Threshold', self.threshold)
        log.add_field('Program', self.program)
        log.add_backref('Manager', self.manager.user)
        return log.formated_log()

class Shop(db.Model, Logger):
    #[Keys and Foreign Keys]
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)

    #[Fields]
    location = db.Column(db.String(int(config["shop"]["location_length"])), nullable=False)
    wallet_address = db.Column(db.String(int(config["shop"]["wallet_address_length"])), nullable=False)
    #maybe monthly earned
    
    #[Relationships]
    cashiers = db.relationship('Cashier', backref='shop', lazy=True)
    transactions = db.relationship('Transaction', backref='receiver', lazy=True)

    def log(self, number_of_spaces=0):
        log = Log("Shop" , number_of_spaces)
        log.add_field('ID', self.id)
        log.add_field('Location', self.location)
        log.add_field('Wallet Address', self.wallet_address)
        #log.add_backref('Brand', self.brand)
        return log.formated_log()

class Transaction(db.Model, Logger):
    #[Keys and Foreign Keys]
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    initiator_id = db.Column(db.Integer, db.ForeignKey('cashier.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)

    #[Fields]
    quantity = db.Column(db.Double, nullable=False)
    date = db.Column(db.Double, nullable=False)
    type = db.Column(Enum(TRANSACTION_TYPE), nullable=False)

    #[Relationships]
    #N/A

    def log(self, number_of_spaces=0):
        log = Log("Transaction" , number_of_spaces)
        log.add_field('ID', self.id)
        log.add_field('Quantity', self.quantity)
        log.add_field('Date', self.date)
        log.add_field('Type', self.type)
        log.add_relation('Sender', self.sender)
        log.add_relation('Receiver', self.receiver)
        log.add_relation('Initiator', self.initiator)
        log.add_relation('Card', self.card)
        return log.formated_log()
