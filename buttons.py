from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from main import tr, db

async def get(language):
    get = InlineKeyboardMarkup(row_width=2)
    get.insert(InlineKeyboardButton(text=tr.translate("Buy",dest=language).text, callback_data='get'))
    get.insert(InlineKeyboardButton(text=tr.translate("🏘 Home",dest=language).text, callback_data='home'))
    return get


async def geto(language):
    get = InlineKeyboardMarkup(row_width=2)
    get.insert(InlineKeyboardButton(text=tr.translate("❌ Delete",dest=language).text, callback_data='delete'))
    return get

async def menu(language):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=tr.translate("Buy", dest=language).text, callback_data="buy"),
                InlineKeyboardButton(text=tr.translate("Sell", dest=language).text, callback_data="sell"),
            ],
            [
                InlineKeyboardButton(text=tr.translate("🛒 Basket", dest=language).text, callback_data="basket"),
                InlineKeyboardButton(text=tr.translate("💸 Currency", dest=language).text, callback_data="currency"),
            ],
            [
                InlineKeyboardButton(text=tr.translate("⚙️ Settings", dest=language).text, callback_data="settings"),
                InlineKeyboardButton(text=tr.translate("My products", dest=language).text, callback_data="products"),
            ]

        ]
    )
    return main
async def currency():
    currencies = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='UZS', callback_data='UZS'),
                InlineKeyboardButton(text='KZT', callback_data='KZT'),
                InlineKeyboardButton(text='GBP', callback_data='GBP')
                
            ],
            [
                InlineKeyboardButton(text='KGS', callback_data='KGS'),
                InlineKeyboardButton(text='TJS', callback_data='TJS'),
                InlineKeyboardButton(text='CNY', callback_data='CNY')
            ],
            [
                InlineKeyboardButton(text='RUB', callback_data='RUB'),
                InlineKeyboardButton(text='EUR', callback_data='EUR'),
                InlineKeyboardButton(text='AED', callback_data='AED')
            ],
            [
                InlineKeyboardButton(text="🏘 Home", callback_data='home')
            ]
        ]
    )
    
    return currencies

async def settings(language):
    setting = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=tr.translate("🔄 Update Profile", dest=language).text, callback_data="user"),
                InlineKeyboardButton(text=tr.translate("🌏 Change language", dest=language).text, callback_data="language"),
            ],
            [
                InlineKeyboardButton(text=tr.translate("☎️ Contact", dest=language).text, callback_data="contact"),
                InlineKeyboardButton(text=tr.translate("🏘 Home", dest=language).text, callback_data="home")
            ]
        ]
    )
    
    return setting


lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [
             
            InlineKeyboardButton("🇬🇧English🇬🇧", callback_data='en'),
            InlineKeyboardButton("🇷🇺Russian🇷🇺", callback_data='ru')
        ],
        [
            InlineKeyboardButton('🇺🇿Uzbek🇺🇿', callback_data="uz"),
            
        ]
    ]

)


async def products(filter, output):
    products = db.select_products(filter,output)
    print(products)
    btn = InlineKeyboardMarkup(row_width=2)
    for i in range(0,len(products)):
        btn.insert(InlineKeyboardButton(text=products[i][1], callback_data=f"Pro_{products[i][0]}"))
    btn.insert(InlineKeyboardButton(text='🏘 Home', callback_data=f"home"))
    return btn

async def all_products():
    products = db.select_all_products()
    print(products)
    btn = InlineKeyboardMarkup(row_width=2)
    for i in range(0,len(products)):
        btn.insert(InlineKeyboardButton(text=products[i][1], callback_data=f"All_{products[i][0]}"))
    btn.insert(InlineKeyboardButton(text='🏘 Home', callback_data=f"home"))
    return btn

async def buy(language):
    filter = {
            'Name of the product':'product_name',
            'Price of the product':'product_price',
            'Exchange':'trade',
            'Region':'region',
            'Date':'date',
            'All Products':'all',
            '🏘Home': 'home'
            }
    buy_button = InlineKeyboardMarkup(row_width=2)
    for key, value in filter.items():
        buy_button.insert(InlineKeyboardButton(text=tr.translate(key,dest=language).text, callback_data=value))
    return buy_button

async def number(language):
    number = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=tr.translate("📲 Phone number", dest=language).text, request_contact=True)
            ]
        ],
        resize_keyboard=True
    )
    
    return number

choose2 = {"✅ Yes": 'yes',"❌ No": 'no'}


async def choose(lan):
    btn = InlineKeyboardMarkup(row_width=2)
    for i,m  in choose2.items():
        btn.insert(InlineKeyboardButton(text=tr.translate(i, dest =lan).text, callback_data=m))
    return btn


rek = {'Email':'email', '📲 Phone number':'phone_number','🏘 Home':'home'}


async def change(language):
    btn = InlineKeyboardMarkup(row_width=2)
    for i,m  in rek.items():
        btn.insert(InlineKeyboardButton(text=tr.translate(i,dest=language).text, callback_data=m))
    return btn




async def basket(user_id):
    product = db.select_cart_id(user_id)
    btn = InlineKeyboardMarkup(row_width=2)
    for i in product:
        btn.insert(InlineKeyboardButton(text=db.select_products_id(i[1])[1], callback_data=i[1]))
    btn.insert(InlineKeyboardButton(text="🏘 Home", callback_data="home"))
    
    return btn

async def my_products(user):
    products = db.select_products_owner(user)
    btn = InlineKeyboardMarkup(row_width=2)
    for i in products:
        btn.insert(InlineKeyboardButton(text=i[1],callback_data=i[0]))
    btn.insert(InlineKeyboardButton(text="🏘 Home", callback_data="home"))
    return btn
        