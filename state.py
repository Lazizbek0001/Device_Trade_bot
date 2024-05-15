from aiogram.dispatcher.filters.state import State, StatesGroup

class RegisterUser(StatesGroup):
    check1 = State()
    email = State()
    email_check = State()
    check = State()
    phone_number = State()
    
class Product(StatesGroup):
    product_name = State()
    product_photo = State()
    description = State()
    trade = State()
    trade_name = State()
    type = State()
    region = State()
    price = State()
    
    
class Currency(StatesGroup):
    currency = State()
    
    
class Settings(StatesGroup):
    setting = State()
    
    language = State()
    
    change = State()
    change2 = State()
    num = State()
    
    
    
class Buy_pro(StatesGroup):
    filter = State()
    output = State()
    check = State()
    check1 = State()
    product = State()
    
class Basket(StatesGroup):
    user_id =State()
    next = State()
    
    
class Myproduct(StatesGroup):
    user_id = State()
    next = State()