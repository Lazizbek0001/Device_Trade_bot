import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config import *
from buttons import *
from data_base import *
from state import *
from api import *
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from googletrans import Translator
import datetime

tr = Translator()

Storage = MemoryStorage()
bot =Bot(token=API_TOKEN)
dp=Dispatcher(bot, storage=Storage)


db = Ed_trade()
db.create_table_prodcuts()
db.create_table_users()
db.create_table_cart()
db.create_table_All_users()


logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    global id
    id = message.from_user.id
    
    user = db.select_users(id)
    if user is None or db.select_all_user(id) is None:
        text = """🇬🇧Please choose a language to continue!
🇷🇺Пожалуйста, выберите язык, чтобы продолжить!
🇺🇿Davom etish uchun tilni tanlang!"""
        await message.answer(text, reply_markup=lang)
        await RegisterUser.check1.set()
    else:
        global language
        language = db.select_all_user(id)[-1]
        await message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))


@dp.callback_query_handler(lambda call: call.data, state= RegisterUser.check1)
async def exo(call : types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    text = "Please enter your email address"
    db.add_to_all_users(id, call.data)
    await state.update_data(check1 = "Something")
    text = tr.translate(text, dest =call.data).text
    
    await call.message.answer(text)
    await RegisterUser.email.set()
    
@dp.message_handler(state=RegisterUser.email)
async def send(message: types.Message, state: FSMContext):
    global language
    language = db.select_all_user(id)
    language = language[-1]
    text = "Please now enter your phone number"
    await state.update_data(email = message.text)
    await message.answer(tr.translate(text, dest=language).text, reply_markup=await number(language))
    await RegisterUser.phone_number.set()    
    
@dp.callback_query_handler(lambda call: call.data)
async def exo(call : types.CallbackQuery):
    await call.message.delete()
    if call.data == 'buy':
        text = "You can filter the products"
        text = tr.translate(text,dest=language).text
        await call.message.answer(text,reply_markup=await buy(language))
        await Buy_pro.filter.set()
    elif call.data == 'sell':
        text = "Enter the name of your product"
        await call.message.answer(tr.translate(text, dest=language).text)
        await Product.product_name.set()
        
    elif call.data == 'currency':
        text = "Please choose a currency"
        await call.message.answer(tr.translate(text,dest=language).text, reply_markup=await currency())
        await Currency.currency.set()
        
    elif call.data == 'settings':
        text = "Please choose to continue"
        text = tr.translate(text,dest= language).text
        await call.message.answer(text, reply_markup=await settings(language))
        await Settings.setting.set()
        
    elif call.data == 'basket':
        text = "Your purchases"
        text = tr.translate(text, dest=language).text
        
        await call.message.answer(text, reply_markup=await basket(db.select_users(id)[0]))
        await Basket.user_id.set()
        
    elif call.data == 'products':
        text = "Your Products"
        text = tr.translate(text, dest=language).text
        await call.message.answer(text, reply_markup=await my_products(db.select_users(id)[0]))
        await Myproduct.user_id.set()
      
      
@dp.callback_query_handler(lambda call:call.data, state=Myproduct.user_id)
async def send(call:types.CallbackQuery, state: FSMContext):
    
    if call.data =='home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
        await state.finish()
        await state.reset_data()
    else:
        print(call.data)
        await call.message.delete()
        products = db.select_products_id(int(call.data))
        text = f"""Name of the product: {products[1]}
    Description of the product: {products[3]}

    You can exchange it with: {products[5]}

    Region: {products[6]}
    Date: {products[7]}
    Product's price: {products[8]}"""
        
        text = tr.translate(text,dest=language).text
        await state.update_data(user_id = int(call.data))
        await call.message.answer_photo(photo=products[2],caption=text,reply_markup=await geto(language))
        await Myproduct.next.set()

@dp.callback_query_handler(lambda call:call.data,state=Myproduct.next)
async def send(call:types.CallbackQuery,state:FSMContext):
    if call.data == 'home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))

    else:
        
        data = await state.get_data()
        pro_id = data.get('user_id')
        await call.message.delete()
        text = "Your products has been removed"
        text = tr.translate(text,dest=language).text
        user = db.select_users(id)[0]
        
        db.delete_product(user, pro_id)
        await call.message.answer(text)
    
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
    await state.finish()
    await state.reset_data()
        
        
        
@dp.callback_query_handler(lambda call:call.data, state=Basket.user_id)
async def send(call:types.CallbackQuery, state: FSMContext):
    
    if call.data =='home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
        await state.finish()
        await state.reset_data()
    else:
        print(call.data)
        await call.message.delete()
        products = db.select_products_id(int(call.data))
        user = db.select_users_id(products[-1])
        text = f"""Name of the product: {products[1]}
Description of the product: {products[3]}

You can exchange it with: {products[5]}

Region: 🌏{products[6]}
Date: {products[7]}
Product's price: 💸{products[8]}
    
Contact: 📲{user[-1]}"""

        text = tr.translate(text,dest=language).text
        await state.update_data(user_id = int(call.data))
        await call.message.answer_photo(photo=products[2],caption=text,reply_markup=await geto(language))
        await Basket.next.set()

@dp.callback_query_handler(lambda call:call.data,state=Basket.next)
async def send(call:types.CallbackQuery,state:FSMContext):
    if call.data == 'home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))

    else:
        data = await state.get_data()
        pro_id = data.get('user_id')
        await call.message.delete()
        text = "Your purchase has been cancelled"
        text = tr.translate(text,dest=language).text
        user = db.select_users(id)[0]
        
        db.delete_cart(user, pro_id)
        await call.message.answer(text)
    
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
    await state.finish()
    await state.reset_data()
       
        
        
@dp.callback_query_handler(lambda call: call.data, state=Currency.currency)
async def exo(call : types.CallbackQuery,state: FSMContext):
    
    await call.message.delete()
    
    if call.data != 'home':
        value = exchange(call.data)
        text = f"1$ will be {value}"
        text = tr.translate(text, dest=language).text
        await call.message.answer(text)

    await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
    await state.finish()
    await state.reset_data()
    

@dp.callback_query_handler(lambda call: call.data, state=Buy_pro.filter)
async def exo(call : types.CallbackQuery,state: FSMContext):
    await state.update_data(filter = call.data)
    await call.message.delete()
    if call.data == 'date':
        text = f"Enter the date like this({datetime.date.today().strftime('%Y-%m-%d')})"
        text = tr.translate(text, dest=language).text
    
        await call.message.answer(text)
        await Buy_pro.output.set()
    elif call.data == 'all':
        text="Products"
        text =tr.translate(text,dest=language).text
        await call.message.answer(text, reply_markup=await all_products())
        await Buy_pro.check.set()
        
        
    elif call.data == 'home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
        await state.finish()
        await state.reset_data()
    else:
        text = f"""Enter the {call.data} you wanted"""
        text = tr.translate(text, dest=language).text
    
        await call.message.answer(text)
        await Buy_pro.output.set()
    
    
@dp.message_handler(state=Buy_pro.output)
async def send(message: types.Message, state: FSMContext):
   
    text = "Results"
    data = await state.get_data()
    filter = data.get('filter')
    output = message.text
    
    await message.answer(tr.translate(text, dest=language).text, reply_markup=await products(filter,output))
    await Buy_pro.check1.set()
    
    
@dp.callback_query_handler(Text(startswith="Pro_"),state=Buy_pro.check1)
async def send(call:types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    if call.data == 'home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
        await state.finish()
        await state.reset_data()
    
    else:
        id = call.data[4:]
        print(id)
        products = db.select_products_id(id)
        user = db.select_users_id(products[-1])
        text = f"""Name of the product: {products[1]}
Description of the product: {products[3]}

You can exchange it with: {products[5]}

Region: 🌏{products[6]}
Date: {products[7]}
Product's price: 💸{products[8]}
    
Contact: 📲{user[-1]}"""

        text = tr.translate(text,dest=language).text
        await state.update_data(check1 = products[0])
        await call.message.answer_photo(photo=products[2],caption=text,reply_markup=await get(language))
        await Buy_pro.product.set()
    
    
    
@dp.callback_query_handler(Text(startswith="All_"),state=Buy_pro.check)
async def send(call:types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    if call.data == 'home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
        await state.finish()
        await state.reset_data()
    else:
        id = call.data[4:]
        print(id)
        products = db.select_products_id(id)
        user = db.select_users_id(products[-1])
        text = f"""Name of the product: {products[1]}
Description of the product: {products[3]}

You can exchange it with: {products[5]}

Region: 🌏{products[6]}
Date: {products[7]}
Product's price: 💸{products[8]}
    
Contact: 📲{user[-1]}"""

        text = tr.translate(text,dest=language).text
        
        await call.message.answer_photo(photo=products[2],caption=text,reply_markup=await get(language))
        await state.update_data(check= products[0])
        await Buy_pro.product.set()




@dp.callback_query_handler(lambda call: call.data, state=Buy_pro.product)
async def exo(call : types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    if call.data == 'home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
        await state.finish()
        await state.reset_data()
    else:
        
        user = db.select_users(id)
        data = await state.get_data()
        product_id = data.get('check')
        pro_id = data.get('check1')
        if pro_id is None:
            db.add_to_cart(user[0],product_id)
        else:
            db.add_to_cart(user[0],pro_id)
        text = f"""Good Purchase"""
        
        await call.message.answer(tr.translate(text, dest=language).text)
        await state.finish()
        await state.reset_data()
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))



@dp.callback_query_handler(lambda call: call.data, state=Settings.setting)
async def exo(call : types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    text = "Please enter your email address"
    if call.data == 'user':
        text = "Please choose a category you want to update"
        await call.message.answer(tr.translate(text, dest=language).text, reply_markup=await change(language))
        await Settings.change.set()
        
    elif call.data == 'language':
        text = "Please choose a language to change into"
        await call.message.answer(tr.translate(text, dest=language).text, reply_markup=lang)
        await Settings.language.set()
    elif call.data == 'contact':
        text = "If you have any questions contact @Laziznormatov or @taj1boev"
        await call.message.answer(tr.translate(text, dest=language).text)
        await state.finish()
        await state.reset_data()
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
    elif call.data == 'home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
        await state.finish()
        await state.reset_data()

@dp.callback_query_handler(lambda call: call.data, state=Settings.language)
async def exo(call : types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    text = "Changes are complete"
    db.update_all_users(id,call.data)
    text = tr.translate(text, dest =call.data).text
    
    await call.message.answer(text)
    await state.finish()
    await state.reset_data()
    global language
    language = db.select_all_user(id)
    language = language[-1]
    await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))

@dp.callback_query_handler(text= 'home')
async def send(call:types.CallbackQuery):
    await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))

@dp.callback_query_handler(lambda call: call.data, state=Settings.change)
async def exo(call : types.CallbackQuery,state: FSMContext):
    await state.update_data(change=call.data)
    await call.message.delete()
    if call.data =='email':
        text = "Please send your new email"
        text = tr.translate(text, dest =language).text
        await call.message.answer(text)
        await Settings.change2.set()
    elif call.data == 'phone_number':
        text = "📲 Enter your phone number "
        text = tr.translate(text, dest =language).text
        await call.message.answer(text, reply_markup=await number(language))
        await Settings.num.set()
    elif call.data == 'home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
        await state.finish()
        await state.reset_data()

@dp.message_handler(content_types='contact',state=Settings.num)
async def send(message: types.Message, state: FSMContext):
    text = "Updates are complete"
    data = await state.get_data()
    change = data.get('change')
    db.update_user(change,message.contact['phone_number'], id)
    await message.answer(tr.translate(text, dest=language).text)
    await state.finish()
    await state.reset_data()
    await message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))

@dp.message_handler(state=Settings.change2)
async def send(message: types.Message, state: FSMContext):
    text = "Updates are complete"
    data = await state.get_data()
    change = data.get('change')
    print(change)
    print(message.text)
    print(id)
    db.update_user(change,message.text, id)
    await message.answer(tr.translate(text, dest=language).text)
    await state.finish()
    await state.reset_data()
    await message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))


        
@dp.message_handler(state=Product.product_name)
async def send(message: types.Message, state: FSMContext):
    text = "Enter product's photo 📸"
    await state.update_data(product_name = message.text)
    await message.answer(tr.translate(text, dest=language).text)
    await Product.product_photo.set()
    
@dp.message_handler(content_types='photo',state=Product.product_photo)
async def send(message: types.Message, state: FSMContext):
    text = "Enter product's description"
    await state.update_data(product_photo = message.photo[-1].file_id)
    await message.answer(tr.translate(text, dest=language).text)
    await Product.description.set()
    
@dp.message_handler(state=Product.description)
async def send(message: types.Message, state: FSMContext):
    text = "Do you want to trade your product"
    await state.update_data(description = message.text)
    await message.answer(tr.translate(text, dest=language).text, reply_markup=await choose(language))
    await Product.trade.set()
    
@dp.callback_query_handler(state=Product.trade)
async def send(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(trade=call.data)
    if call.data == 'yes':
        await call.message.answer(tr.translate("Enter the name of the product",dest=language).text)
        await Product.trade_name.set()
    elif call.data == 'no':
        await call.message.answer(tr.translate("Enter the name of the city you live in", dest=language).text)
        await Product.region.set()
    elif call.data == 'home':
        await call.message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
        await state.finish()
        await state.reset_data()

@dp.message_handler(state=Product.trade_name)
async def send(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(trade_name=message.text)
    await message.answer(tr.translate("Enter the name of the city you live in",dest=language).text)
    await Product.region.set()
     
        
@dp.message_handler(state=Product.region)
async def send(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(region=message.text)
    await message.answer(tr.translate("Enter the price of the product \nNote it will be added as US currency",dest=language).text)
    await Product.price.set()
    
@dp.message_handler(state=Product.price)
async def send(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    product_name = str(data.get('product_name'))
    product_photo = str(data.get('product_photo'))
    description = str(data.get('description'))
    trade = data.get('trade')
    trade_name = data.get('trade_name')
    region = str(data.get('region'))
    price = str(data.get('price'))
    date = datetime.date.today()
    date = date.strftime('%Y-%m-%d')
    id = db.select_users(message.from_user.id)[0]
    db.add_products(product_name,product_photo,description,trade,trade_name, region,str(date),price,str(id))
    await message.answer(tr.translate("Your product has been to the database",dest=language).text)
    await message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
    await state.finish()
    await state.reset_data()
   

    
@dp.message_handler(content_types=  "contact",state=RegisterUser.phone_number)
async def send(message: types.Message, state: FSMContext):


    data = await state.get_data()
    email = data.get('email')
    phone_number = message.contact['phone_number']    
    id = message.from_user.id
    username = message.from_user.username
    db.add_users(id,username,email, phone_number)
    await state.finish()
    await state.reset_data()
    await message.answer(tr.translate("Your information has been added to the database",dest=language).text,reply_markup=ReplyKeyboardRemove())
    await message.answer(tr.translate("Menu", dest=language).text, reply_markup=await menu(language))
    

        
        






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)