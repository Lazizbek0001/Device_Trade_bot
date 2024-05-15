import sqlite3



conn = sqlite3.connect("data_base.db")

cur = conn.cursor()


class Ed_trade:
    def __init__(self):
        self.conn = conn
        self.cur = cur
        
    def create_table_All_users(self):
        cur.execute("""create table if not exists All_users (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        telegram_id INT,
                        language varchar(5)
                        )""")

    def create_table_prodcuts(self):
        cur.execute("""create table if not exists products (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_name varchar(50),
                        product_photo varchar(40),
                        product_description varchar(300),
                        trade varchar(40),
                        trade_name varchar(50),
                        region varchar(40),
                        date varchar(40),
                        product_price varchar(40),
                        owner_id INT
                        )""")
        conn.commit()
        
    def create_table_users(self):
        cur.execute("""create table if not exists users (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        telegram_id INT,
                        username varchar(50),
                        email varchar(50),
                        phone_number varchar(25)
                        )""")
        conn.commit()
        
    def create_table_cart(self):
        cur.execute("""create table if not exists cart (
                        User_id INT,
                        Product_id INT
                        )""")
        conn.commit()
        
    def select_cart(self):
        self.cur.execute("select * from cart")
        res = self.cur.fetchall()
        return res
        
    def add_to_cart(self, User_id, Product_id):
        carts = self.select_cart()
        for i in carts:
            if User_id not in i and Product_id not in i:
                self.cur.execute(f"insert into cart (User_id, Product_id) values ({int(User_id)}, {int(Product_id)})")
                self.conn.commit()
            
    def add_users(self,telegram_id, username, email, phone_number):
        self.cur.execute(f"insert into users(telegram_id, username,  email, phone_number) values({telegram_id}, '{username}', '{email}', '{phone_number}')")
        self.conn.commit()
         
    def add_products(self,product_name, product_photo, product_desc, trade, trade_name, region, date, product_price, owner_id):
     
        self.cur.execute(f"insert into products(product_name, product_photo, product_description, trade, trade_name, region, date, product_price, owner_id) values('{product_name}', '{product_photo}', '{product_desc}', '{trade}', '{trade_name}', '{region}', '{date}', '{product_price}', {owner_id})")  
        self.conn.commit()
        
        
    def select_products(self,old,new):
        self.cur.execute(f"select * from products where {old} like '{new}%' ")
        res = self.cur.fetchall()
        return res
    
    def select_products_id(self,id):
        self.cur.execute(f"select * from products where Id = {id}")
        res = self.cur.fetchone()
        return res
    def select_products_owner(self,id):
        self.cur.execute(f"select * from products where owner_id = {id}")
        res = self.cur.fetchall()
        return res
    
    def select_all_products(self):
        self.cur.execute("select * from products")
        res = self.cur.fetchall()
        return res
    
    def select_users(self,telegram_id):
        self.cur.execute("select * from users where telegram_id = {}".format(telegram_id))
        res = self.cur.fetchone()
        return res

    def select_all_user(self,telegram_id):
        self.cur.execute("""select * from All_users where telegram_id = {}""".format(telegram_id))
        user = self.cur.fetchone()
        return user
    
    def add_to_all_users(self, telegram_id, language):
        self.user = self.select_all_user(telegram_id)
        if self.user is None:
            self.cur.execute(f"insert into All_users(telegram_id,language) values({telegram_id}, '{language}')")
            self.conn.commit()
            
            
    def update_all_users(self, telegram_id, language):
        self.cur.execute("update All_users set language = '{}' where telegram_id= {}".format(language, telegram_id))
        self.conn.commit()
            
            
    def update_user(self, old, new, id):
        self.cur.execute("update users set '{}' = '{}' where telegram_id= {}".format(old, new, id))
        self.conn.commit()

    def delete_cart(self,user, product):
        self.cur.execute(f"delete from cart where User_id = {user} and Product_id = {product}")
        self.conn.commit()
        
    def select_cart_id(self,id):
        self.cur.execute(f"select * from cart where User_id = {id}")
        res = self.cur.fetchall()
        return res
    
    
    def delete_product(self,owner, pro_id):
        self.cur.execute(f"delete from products where owner_id = {owner} and Id = {pro_id}")
        self.conn.commit()
        
    def select_users_id(self, id):
        self.cur.execute(f"select * from users where Id = {id}")
        res = self.cur.fetchone()
        return res