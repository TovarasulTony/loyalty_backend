import enum


class USER_TYPE(enum.Enum):
    Invalid = -1
    User = "User"
    Cashier = "Cashier"
    Manager = "Manager"

class BRAND_TYPE(enum.Enum):
    Invalid = -2
    Food = "Food"
    Retail = "Retail"
    Beauty = "Beauty"
    Services = "Services"
    Healthcare = "Healthcare"

class TRANSACTION_TYPE(enum.Enum):
    Invalid = -3
    User2App = "U2A"
    App2User = "A2U"
