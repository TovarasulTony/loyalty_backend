from sqlalchemy import Enum
from flask_api import db, config
from flask_api.enums import USER_TYPE, BRAND_TYPE, TRANSACTION_TYPE

class User(db.Model):
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

    def __repr__(self):
        return (
                    '{ User }\n'
                    '---------\n'
                    f'[ID]: {self.id}\n'
                    #f'[User Type]: {self.type}\n'
                    f'[Nickname]: {self.nickname}\n'
                    f'[Wallet Address]: {self.wallet_address}\n'
                )

class Cashier(db.Model):
    #[Keys and Foreign Keys]
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)

    #[Fields]
    #N/A

    #[Relationships]
    transactions = db.relationship('Transaction', backref='initiator', lazy=True)

    def __repr__(self):
        return (
                    '{ Cashier }\n'
                    '---------\n'
                    f'[ID]: {self.id}\n'
                    f'[Shop]: {self.shop}\n'
                )

class Manager(db.Model):
    #[Keys and Foreign Keys]
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #[Fields]
    #N/A

    #[Relationships]
    #user = db.relationship('User', backref='manager', lazy=True)
    brand = db.relationship('Brand', backref='manager', lazy=True)
    #transactions = db.relationship('Transaction', backref='initiator', lazy=True)

    def __repr__(self):
        return (
                    '{ Manager }\n'
                    '---------\n'
                    f'[ID]: {self.id}\n'
                    f'[Brand Name]: {self.brand.name}\n'
                )

class Card(db.Model):
    #[Keys and Foreign Keys]
    id = db.Column(db.Integer, primary_key=True)
    holder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)

    #[Fields]
    #N/A

    #[Relationships]
    transactions = db.relationship('Transaction', backref='card', lazy=True)

    def __repr__(self):
        return (
                    '{ Card }\n'
                    '---------\n'
                    f'[ID]: {self.id}\n'
                    f'[Holder]: {self.holder}\n'
                    f'[Brand]: {self.brand}\n'
                    f'[Wallet Address]: {self.wallet_address}\n'
                )

class Brand(db.Model):
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

    def __repr__(self):
        return (
                    '{ Brand }\n'
                    '---------\n'
                    f'[ID]: {self.id}\n'
                    f'[Name]: {self.name}\n'
                    f'[Type]: {self.type}\n'
                    f'[Threshold]: {self.threshold}\n'
                    f'[Program]: {self.program}\n'
                )

class Shop(db.Model):
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

    def __repr__(self):
        return (
                    '{ Shop }\n'
                    '---------\n'
                    f'[ID]: {self.id}\n'
                    f'[Location]: {self.location}\n'
                    f'[Wallet_address]: {self.wallet_address}\n'
                    f'[Brand]: {self.brand}\n'
                )

class Transaction(db.Model):
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

    def __repr__(self):
        return (
                    '{ Transaction }\n'
                    '---------\n'
                    f'[ID]: {self.id}\n'
                    f'[Quantity]: {self.quantity}\n'
                    f'[Date]: {self.date}\n'
                    f'[Type]: {self.type}\n'
                    f'    [Sender]: {self.sender}\n'
                    f'    [Receiver]: {self.receiver}\n'
                    f'    [Initiator]: {self.initiator}\n'
                    f'    [Card]: {self.card}\n'
                )
