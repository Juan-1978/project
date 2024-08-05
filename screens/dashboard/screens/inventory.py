from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.divider import MDDivider
from kivy.metrics import dp
import sqlite3
import math


def create_table(self):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS test_table_3(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL DEFAULT 0.00,
        quantity INT NOT NULL,
        on_order INT DEFAULT 0,  
        on_sales_order INT DEFAULT 0,
        work_in_progress INT DEFAULT 0,
        sale_price REAL DEFAULT 0.00
        )
    """)

    conn.commit()
    conn.close()


def add_item(self):
    category = self.ids.add_cat_btn.text
    name = self.ids.item_name.text_input.text
    #category = self.ids.item_cat.text_input.text
    description = self.ids.item_des.text_input.text
    price = float(self.ids.item_price.text_input.text) if self.ids.item_price.text_input.text else 0.00
    quantity = int(self.ids.item_qua.text_input.text) if self.ids.item_qua.text_input.text else 0
    on_order = int(self.ids.item_order.text_input.text) if self.ids.item_order.text_input.text else 0
    on_sales_order = int(self.ids.item_sales.text_input.text) if self.ids.item_sales.text_input.text else 0
    work_in_progress = int(self.ids.item_work.text_input.text) if self.ids.item_work.text_input.text else 0
    sale_price = float(self.ids.item_sale_price.text_input.text) if self.ids.item_sale_price.text_input.text else 0.00

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    print(category)

    if category == 'Finished Goods':
         c.execute("INSERT INTO test_table_3 (name, category, description, price, work_in_progress, on_sales_order, sale_price, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, category, description, price, work_in_progress, on_sales_order, sale_price, quantity)
        )
    else:
        c.execute("INSERT INTO test_table_3 (name, category, description, price, on_order, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            (name, category, description, price, on_order, quantity)
        )

    conn.commit()
    conn.close()
    
    self.ids.add_cat_btn.text = 'Select Category'
    self.ids.item_name.text_input.text = ''
    self.ids.item_des.text_input.text = ''
    self.ids.item_price.text_input.text = ''
    self.ids.item_qua.text_input.text = ''
    self.ids.item_order.text_input.text = ''
    self.ids.item_sales.text_input.text = ''
    self.ids.item_work.text_input.text = ''
    self.ids.item_sale_price.text_input.text = ''
    card = self.ids.add_item_card
    goods_sales = self.ids.item_sales
    goods_work = self.ids.item_work
    goods_price = self.ids.item_sale_price
    submit = self.ids.add_submit
    card.opacity = 0
    goods_price.opacity = 0
    goods_sales.opacity = 0
    goods_work.opacity = 0
    submit.opacity = 0


def show_add_card(self):
    category = self.ids.add_cat_btn.text
    card = self.ids.add_item_card
    goods_sales = self.ids.item_sales
    goods_work = self.ids.item_work
    goods_price = self.ids.item_sale_price
    submit = self.ids.add_submit

    if category == 'Finished Goods':
        card.opacity = 1
        goods_price.opacity = 1
        goods_sales.opacity = 1
        goods_work.opacity = 1
        submit.opacity = 1
    else:
        card.opacity = 1
        goods_price.opacity = 0
        goods_sales.opacity = 0
        goods_work.opacity = 0
        submit.opacity = 1
    

def display_table(self):
    table = self.ids.table_box
    table_head = self.ids.table_head
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, name, category, description, price, quantity FROM test_table_3")
    items = c.fetchall()
    conn.close()

    table.clear_widgets() 
    table_head.clear_widgets() 

    head = ['Id', 'Name', 'Category', 'Description', 'Price', 'Quantity'] 

    table_head.add_widget(MDLabel(text='Edit | Delete', halign='center')) 

    for i in head:
        row = MDLabel(text=i, md_bg_color='lightgray', halign='center', bold=True)
        table_head.add_widget(row)

    paginated_grid = PaginatedGrid(cols=7, items=items, items_per_page=6)
    table.add_widget(paginated_grid)

    prev_btn = self.ids.prev_btn
    next_btn = self.ids.next_btn
    prev_btn.on_press = paginated_grid.prev_page
    next_btn.on_press = paginated_grid.next_page


def edit_item(self):
    plus_btn = self.ids.plus_btn
    edit_btn = self.ids.edit_btn
    delete_btn = self.ids.delete_btn

    plus_btn.opacity = 1
    edit_btn.opacity = 0
    delete_btn.opacity = 0

    print(f'Editing {self}')


def delete_item(self):
    plus_btn = self.ids.plus_btn
    edit_btn = self.ids.edit_btn
    delete_btn = self.ids.delete_btn

    plus_btn.opacity = 1
    edit_btn.opacity = 0
    delete_btn.opacity = 0

    print(f'Deleting {self}')

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
            

class CategoryButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = [
            "Asset", "Component", "Raw Material", 
            "Finished Goods", "Maintenance", "Packing"
        ]
        self.on_release = self.show_menu
        self.menu = None

    def show_menu(self):
        if not self.menu:
            menu_items = [{'text': item, 'on_release': lambda x=item: self.set_item(x)} for item in self.items]
            self.menu = MDDropdownMenu(
                caller=self,
                items=menu_items,
                width_mult=4
            )
        self.menu.open()

    def set_item(self, item):
        self.text = item
        if self.menu:
            self.menu.dismiss()
            self.menu = None  


class PaginatedGrid(MDGridLayout):
    items = ListProperty()
    page = NumericProperty(0)
    items_per_page = NumericProperty(6)
    checked_box = ObjectProperty(None, allow_none=True)
    page_id = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_grid()
        
    def checkbox_click(self, checkbox, value):
        parent_widget = self.parent.parent.parent
        plus_btn = parent_widget.ids.get('plus_btn')
        edit_btn = parent_widget.ids.get('edit_btn')
        delete_btn = parent_widget.ids.get('delete_btn')
        
        if value:
            plus_btn.opacity = 0
            edit_btn.opacity = 1
            delete_btn.opacity = 1
            if self.checked_box and self.checked_box != checkbox:
                self.checked_box.active = False
            self.checked_box = checkbox
        else:
            if self.checked_box == checkbox:
                self.checked_box.active = False
                plus_btn.opacity = 1
                edit_btn.opacity = 0
                delete_btn.opacity = 0

    def update_grid(self):
        self.clear_widgets()
        start = self.page * self.items_per_page
        end = start + self.items_per_page

        for item in self.items[start:end]:
            #value = item[4] * item[5]
            checkbox = CheckBox(group='group', color=(0, 0, 0, 1))
            checkbox.bind(active=self.checkbox_click)
            self.add_widget(checkbox)
            #updated_item = item + (value,)
            #item = updated_item
            updated_item = ('ID-' + str(item[0]),) + item[1:]
            for i in updated_item:
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
            label_text = self.parent.parent.parent.ids.page_id
            label_text.text = self.page_id
        except AttributeError:
            print("Could not find the parent or label with ID 'page_id'.")