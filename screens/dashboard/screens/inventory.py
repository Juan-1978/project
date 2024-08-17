from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.divider import MDDivider
from kivy.metrics import dp
import sqlite3
import math
from components import KV_NO_INPUT, KV_NOT_FOUND, KV_EXIST, KV_NOT_ENOUGH

def create_table(self):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL DEFAULT 0.00,
        quantity INT NOT NULL,
        on_order INT DEFAULT 0,  
        on_sales_order INT DEFAULT 0,
        work_in_progress INT DEFAULT 0,
        sale_price REAL DEFAULT 0.00,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INT NOT NULL,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS incomes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sale_price REAL NOT NULL,
        quantity INT NOT NULL,
        buyer TEXT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_item(self):
    category = self.ids.add_cat_btn.text
    name = self.ids.item_name.text_input.text
    description = self.ids.item_des.text_input.text
    price = float(self.ids.item_price.text_input.text) if self.ids.item_price.text_input.text else 0.00
    quantity = int(self.ids.item_qua.text_input.text) if self.ids.item_qua.text_input.text else 0
    on_order = int(self.ids.item_order.text_input.text) if self.ids.item_order.text_input.text else 0
    work_in_progress = int(self.ids.item_work.text_input.text) if self.ids.item_work.text_input.text else 0
    sale_price = float(self.ids.item_sale_price.text_input.text) if self.ids.item_sale_price.text_input.text else 0.00

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if name == '':
        card = Builder.load_string(KV_NO_INPUT) 
        parent_widget = self.parent.parent.parent
        parent_widget.add_widget(card)
    else:
        try:
            if category == 'Finished Goods':
                c.execute("INSERT INTO inventory (name, category, description, price, work_in_progress, sale_price, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, category, description, price, work_in_progress, sale_price, quantity)
                )
            else:
                c.execute("INSERT INTO inventory (name, category, description, price, on_order, quantity) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, category, description, price, on_order, quantity)
                )
                if category == 'Component' or category == 'Raw Material':
                    c.execute("INSERT INTO expenses (name, type, price, quantity) VALUES (?, ?, ?, ?)", (name, 'Manufacturing', price, quantity + on_order))
                else:
                    c.execute("INSERT INTO expenses (name, type, price, quantity) VALUES (?, ?, ?, ?)", (name, 'Operational', price, quantity + on_order))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            card = Builder.load_string(KV_EXIST) 
            parent_widget = self.parent.parent.parent
            parent_widget.add_widget(card)
            print(f"An unexpected error occurred: {e}")
    
    self.ids.add_cat_btn.text = 'Select Category'
    self.ids.item_name.text_input.text = ''
    self.ids.item_des.text_input.text = ''
    self.ids.item_price.text_input.text = ''
    self.ids.item_qua.text_input.text = ''
    self.ids.item_order.text_input.text = ''
    #self.ids.item_sales.text_input.text = ''
    self.ids.item_work.text_input.text = ''
    self.ids.item_sale_price.text_input.text = ''
    card = self.ids.add_item_card
    #goods_sales = self.ids.item_sales
    goods_work = self.ids.item_work
    goods_price = self.ids.item_sale_price
    submit = self.ids.add_submit
    card.opacity = 0
    goods_price.opacity = 0
    #goods_sales.opacity = 0
    goods_work.opacity = 0
    submit.opacity = 0
    submit.disabled = True

    self.display_table()


def show_add_card(self):
    category = self.ids.add_cat_btn.text
    card = self.ids.add_item_card
    price = self.ids.item_price
    on_order = self.ids.item_order
    #goods_sales = self.ids.item_sales
    goods_work = self.ids.item_work
    goods_price = self.ids.item_sale_price
    submit = self.ids.add_submit

    if category == 'Finished Goods':
        card.opacity = 1
        price.opacity = 0
        price.disabled = True
        on_order.opacity = 0
        on_order.disabled = True
        goods_price.opacity = 1
        #goods_sales.opacity = 1
        goods_work.opacity = 1
        submit.opacity = 1
        submit.disabled = False
    else:
        card.opacity = 1
        price.opacity = 1
        price.disabled = False
        on_order.opacity = 1
        on_order.disabled = False
        goods_price.opacity = 0
        #goods_sales.opacity = 0
        goods_work.opacity = 0
        submit.opacity = 1
        submit.disabled = False


def close_add_card(self):
    card = self.ids.add_item_card
    self.ids.add_cat_btn.text = 'Select Category'
    self.ids.item_name.text_input.text = ''
    self.ids.item_des.text_input.text = ''
    self.ids.item_price.text_input.text = ''
    self.ids.item_qua.text_input.text = ''
    self.ids.item_order.text_input.text = ''
    #self.ids.item_sales.text_input.text = ''
    self.ids.item_work.text_input.text = ''
    self.ids.item_sale_price.text_input.text = ''
    card.opacity = 0
    

def display_table(self):
    table = self.ids.table_box
    table_head = self.ids.table_head
    button_text = self.ids.button_text.text

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    category = button_text.strip() 
    table.clear_widgets() 
    table_head.clear_widgets()

    if category == 'All':
        c.execute("SELECT strftime('%Y-%m-%d', date), name, category, description, price, on_order, quantity FROM inventory")
        head = ['Date', 'Name', 'Category', 'Description', 'Price', 'On Order', 'Quantity'] 
    elif category == 'Finished Goods':
        c.execute("SELECT strftime('%Y-%m-%d', date), name, category, description, quantity, on_sales_order, work_in_progress, sale_price FROM inventory WHERE category = ?", (category,))
        head = ['Date', 'Name', 'Category', 'Description', 'Quantity', 'On Sales Order', 'Work in Progress', 'Sale Price'] 
    else: 
        c.execute("SELECT strftime('%Y-%m-%d', date), name, category, description, price, on_order, quantity FROM inventory WHERE category = ?", (category,))
        head = ['Date', 'Name', 'Category', 'Description', 'Price', 'On Order', 'Quantity'] 
    
    items = c.fetchall()
    conn.close()

    table_head.add_widget(MDLabel(text='Edit | Delete', halign='center')) 

    for i in head:
        row = MDLabel(text=i, md_bg_color='lightgray', halign='center', bold=True)
        table_head.add_widget(row)

    if category == 'Finished Goods':
        paginated_grid = PaginatedGrid(cols=9, items=items, items_per_page=10)
    else:
        paginated_grid = PaginatedGrid(cols=8, items=items, items_per_page=10)
    
    table.add_widget(paginated_grid)

    prev_btn = self.ids.prev_btn
    next_btn = self.ids.next_btn
    plus_btn = self.ids.plus_btn
    edit_btn = self.ids.edit_btn
    delete_btn = self.ids.delete_btn
    prev_btn.on_press = paginated_grid.prev_page
    next_btn.on_press = paginated_grid.next_page
    plus_btn.opacity = 1
    edit_btn.opacity = 0
    delete_btn.opacity = 0
    plus_btn.disabled = False
    edit_btn.disabled = True
    delete_btn.disabled = True


def delete_item(self):
    plus_btn = self.ids.plus_btn
    edit_btn = self.ids.edit_btn
    delete_btn = self.ids.delete_btn

    state = GlobalState()
    current_item = state.get_current_item()
    edit_id = current_item[1]

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE name = ?", (edit_id,))
    
    conn.commit()
    conn.close()

    plus_btn.opacity = 1
    edit_btn.opacity = 0
    delete_btn.opacity = 0
    plus_btn.disabled = False
    edit_btn.disabled = True
    delete_btn.disabled = True

    self.display_table()

class CustomRow(MDBoxLayout):
    text = StringProperty('')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.divider = MDDivider()
        self.label = MDLabel()

    @property
    def halign_value(self):
        try:
            float(self.text)
            return 'right'
        except ValueError:
            return 'center'
           

class PaginatedGrid(MDGridLayout):
    items = ListProperty()
    cols = NumericProperty(8)
    page = NumericProperty(0)
    items_per_page = NumericProperty(10)
    checked_box = ObjectProperty(None, allownone=True)
    page_id = StringProperty()
    current_item = ObjectProperty(None, allownone=True) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_grid()
        
    def checkbox_click(self, checkbox, value):
        self.current_item = None
        plus_btn = None
        edit_btn = None
        delete_btn = None
        try:
            parent_widget = self.parent.parent.parent
            plus_btn = parent_widget.ids.get('plus_btn')
            edit_btn = parent_widget.ids.get('edit_btn')
            delete_btn = parent_widget.ids.get('delete_btn')
        except AttributeError:
            Clock.schedule_once(lambda dt: self.checkbox_click(checkbox, value), 0.1)
            return
        
        state = GlobalState()
        
        if value:
            self.current_item = getattr(checkbox, 'item', None) 
            state.set_current_item(self.current_item)
            if plus_btn:
                plus_btn.opacity = 0
                plus_btn.disabled = True
            if edit_btn:
                edit_btn.opacity = 1
                edit_btn.disabled = False
            if delete_btn:
                delete_btn.opacity = 1
                delete_btn.disabled = False
            if self.checked_box and self.checked_box != checkbox:
                self.checked_box.active = False
            self.checked_box = checkbox
        else:
            if self.checked_box == checkbox:
                self.checked_box = None 
                if plus_btn:
                    plus_btn.opacity = 1
                    plus_btn.disabled = False
                if edit_btn:
                    edit_btn.opacity = 0
                    edit_btn.disabled = True
                if delete_btn:
                    delete_btn.opacity = 0
                    delete_btn.disabled = True

    def update_grid(self):
        self.clear_widgets()
        start = self.page * self.items_per_page
        end = start + self.items_per_page

        for item in self.items[start:end]:
            checkbox = CheckBox(group='group', color=(0, 0, 0, 1))
            checkbox.item = item 
            checkbox.bind(active=self.checkbox_click)
            self.add_widget(checkbox)
            for i in item:
                row = CustomRow(text=str(i))
                self.add_widget(row) 
            
        Clock.schedule_once(self.update_page, 0.1)

    def next_page(self):
        if (self.page + 1) * self.items_per_page < len(self.items):
            self.page += 1
            self.update_grid()

    def prev_page(self): 
        if self.page > 0:
            self.page -= 1
            self.update_grid() 

    def update_page(self, *args):
        rounded_pages = math.ceil(len(self.items)/self.items_per_page)
        self.page_id = f'{self.page + 1}/{rounded_pages}'
        try:
            label = self.parent.parent.parent.ids.page_id
            label.text = self.page_id
        except AttributeError:
            print("Could not find the parent or label with ID 'page_id'.")

    def update_columns(self, num_cols):
        self.cols = num_cols
            

class GlobalState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalState, cls).__new__(cls)
            cls._instance.current_item = None
        return cls._instance

    def set_current_item(self, item):
        self.current_item = item

    def get_current_item(self):
        return self.current_item
    

def load_editing_item(self):
    name = self.ids.edit_name
    category = self.ids.edit_cat
    on_order = self.ids.edit_order
    quantity = self.ids.edit_qua
    sales = self.ids.edit_sales
    work = self.ids.edit_work
    price = self.ids.edit_sale_price

    name_text = name.text_input
    category_text = category.text_input

    state = GlobalState()
    current_item = state.get_current_item()
    name_text.text = current_item[1]
    category_text.text = current_item[2]

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT on_order, work_in_progress, on_sales_order, sale_price, quantity FROM inventory WHERE name LIKE ?", (name_text.text,))
    current = c.fetchone()

    if current:
        current_order, current_work, current_sales, current_sale_price, current_quantity = current
        on_order.text = 'On order: ' + str(current_order)
        quantity.text = 'Quantity: ' + str(current_quantity)       
    else:
        print('Item not found')

    if category_text.text == 'Finished Goods':
        on_order.opacity = 0
        sales.opacity = 1
        work.opacity = 1
        price.opacity = 1
        sales.text = 'On Sales Order: ' + str(current_sales)
        work.text = 'Work In Progress: ' + str(current_work)
        price.text = 'Sale Price: ' + str(current_sale_price)
        
    else:
        on_order.opacity = 1
        sales.opacity = 0
        work.opacity = 0
        price.opacity = 0
        
    conn.close()


def save_edited_item(self):
    name = self.ids.edit_name
    category = self.ids.edit_cat
    desc = self.ids.edit_des
    on_order = self.ids.edit_order
    quantity = self.ids.edit_qua
    sales = self.ids.edit_sales
    work = self.ids.edit_work
    price = self.ids.edit_sale_price

    name_text = name.text_input
    category_text = category.text_input
    desc_text = desc.text_input
    on_order_text = on_order.text_input
    quantity_text = quantity.text_input
    sales_text = sales.text_input
    work_text = work.text_input
    price_text = price.text_input

    state = GlobalState()
    current_item = state.get_current_item()
    name_text.text = current_item[1]
    category_text.text = current_item[2]

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT description, on_order, work_in_progress, on_sales_order, sale_price, quantity FROM inventory WHERE name LIKE ?", (name_text.text,))
    current = c.fetchone()

    if current:
        current_desc, current_order, current_work, current_sales, current_sale_price, current_quantity = current

    new_desc = desc_text.text if desc_text.text != '' else current_desc
    new_order = int(on_order_text.text) if on_order_text.text != '' else current_order
    new_work = int(work_text.text) if work_text.text != '' else current_work
    new_sales = int(sales_text.text) if sales_text.text != '' else current_sales
    new_sale_price = float(price_text.text) if price_text.text != '' else current_sale_price
    new_quantity = current_quantity - new_sales if quantity_text.text == '' else int(quantity_text.text)
    
    if category_text.text == 'Finished Goods':
        update = """
        UPDATE inventory
        SET description = ?, work_in_progress = ?, on_sales_order = ?, sale_price = ?, quantity = ?
        WHERE name = ?; 
        """
        if new_quantity < 0:
            card = Builder.load_string(KV_NOT_ENOUGH) 
            parent_widget = self.parent.parent.parent
            parent_widget.add_widget(card)
        else:
            c.execute(update, (new_desc, new_work, 0, new_sale_price, new_quantity, name_text.text))
            if sales_text.text != '' and new_sales > 0:
                c.execute("INSERT INTO incomes (name, sale_price, quantity) VALUES (?, ?, ?)", (name_text.text, new_sale_price, new_sales))
    else:
        update = """
        UPDATE inventory
        SET description = ?, on_order = ?, quantity = ?
        WHERE name = ?; 
        """
        c.execute(update, (new_desc, new_order, new_quantity, name_text.text))

        exp_quantity = (new_quantity + new_order) - current_quantity
        if isinstance(exp_quantity, int) and exp_quantity + new_order > 0:
            c.execute("SELECT price FROM inventory WHERE name = ?", (name_text.text,))
            exp_price = c.fetchone()
            if category_text.text == 'Component' or category_text.text == 'Raw Material':
                c.execute("INSERT INTO expenses (name, type, price, quantity) VALUES (?, ?, ?, ?)", (name_text.text, 'Manufacturing', exp_price[0], exp_quantity + new_order))
            else:
                c.execute("INSERT INTO expenses (name, type, price, quantity) VALUES (?, ?, ?, ?)", (name_text.text, 'Operational', exp_price[0], exp_quantity + new_order))
            
    conn.commit()
    conn.close()

    desc_text.text = ''
    on_order_text.text = ''
    quantity_text.text = ''
    sales_text.text = ''
    work_text.text = ''
    price_text.text = ''

    self.display_table()


def close_edit_card(self):
    desc = self.ids.edit_des
    on_order = self.ids.edit_order
    quantity = self.ids.edit_qua
    sales = self.ids.edit_sales
    work = self.ids.edit_work
    price = self.ids.edit_sale_price

    desc_text = desc.text_input
    on_order_text = on_order.text_input
    quantity_text = quantity.text_input
    sales_text = sales.text_input
    work_text = work.text_input
    price_text = price.text_input

    desc_text.text = ''
    on_order_text.text = ''
    quantity_text.text = ''
    sales_text.text = ''
    work_text.text = ''
    price_text.text = ''


def find_item(self):
    name = self.ids.name_input.text.strip()
    table = self.ids.table_box
    table_head = self.ids.table_head

    if name:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM inventory WHERE name LIKE ?", (name,))
        is_found = c.fetchone()
        if is_found:
            self.ids.button_text.text = ''
            table.clear_widgets() 
            table_head.clear_widgets()
            category = is_found[2]
            if category == 'Finished Goods':
                head = ['Date', 'Name', 'Category', 'Description', 'Quantity', 'On Sales Order', 'Work in Progress', 'Sale Price'] 
                new_tuple = tuple(x for x in is_found if  x != is_found[4] and x != is_found[6])
            else: 
                head = ['Date', 'Name', 'Category', 'Description', 'Price', 'Quantity', 'On Order'] 
                new_tuple = is_found[:7]
    
            items = []
            items.append(new_tuple)
            conn.close()

            table_head.add_widget(MDLabel(text='Edit | Delete', halign='center')) 

            for i in head:
                row = MDLabel(text=i, md_bg_color='lightgray', halign='center', bold=True)
                table_head.add_widget(row)

            if category == 'Finished Goods':
                paginated_grid = PaginatedGrid(cols=9, items=items, items_per_page=10)
            else:
                paginated_grid = PaginatedGrid(cols=8, items=items, items_per_page=10)
    
            table.add_widget(paginated_grid)   
        else:
            card = Builder.load_string(KV_NOT_FOUND) 
            parent_widget = self.parent.parent.parent
            parent_widget.add_widget(card)
    else:
        card = Builder.load_string(KV_NO_INPUT) 
        parent_widget = self.parent.parent.parent
        parent_widget.add_widget(card)

    self.ids.name_input.text = ''
        