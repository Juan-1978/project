from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.divider import MDDivider
import math
import sqlite3


def show_exp(self):
    financial_box = self.ids.financial_box
    exp_box = self.ids.exp_box
    back_btn = self.ids.back_btn
    plus_btn = self.ids.plus_exp_btn

    financial_box.opacity = 0
    financial_box.disabled = True
    exp_box.opacity = 1
    exp_box.disabled = False
    back_btn.opacity = 1
    back_btn.disabled = False
    plus_btn.opacity = 1
    plus_btn.disabled = False

    self.display_exp()


def go_back(self):
    financial_box = self.ids.financial_box
    exp_box = self.ids.exp_box
    button = self.ids.back_btn
    plus_btn = self.ids.plus_exp_btn

    financial_box.opacity = 1
    financial_box.disabled = False
    exp_box.opacity = 0
    exp_box.disabled = True
    button.opacity = 0
    button.disabled = True
    plus_btn.opacity = 0
    plus_btn.disabled = True


class SheetGrid(MDGridLayout):
    items = ListProperty()
    cols = NumericProperty(6)
    page = NumericProperty(0)
    items_per_page = NumericProperty(10)
    page_id = StringProperty()
    current_item = ObjectProperty(None, allownone=True) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_grid()

    def update_grid(self):
        self.clear_widgets()
        self.total = 0
        start = self.page * self.items_per_page
        end = start + self.items_per_page

        for item in self.items[start:end]:
            value = item[3] * item[4]
            updated_item = item + (value,)
            for i in updated_item:
                row = ExpensesRow(text=str(i))
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
            label = self.parent.parent.parent.ids.exp_id
            label.text = self.page_id
        except AttributeError:
            print("Could not find the parent or label with ID 'page_id'.")

    def update_columns(self, num_cols):
        self.cols = num_cols


class ExpensesRow(MDBoxLayout):
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
        

def display_exp(self):
    sheet_head = self.ids.sheet_head
    sheet_box = self.ids.sheet_box
    type = self.ids.type_btn.text

    conn = sqlite3.connect('database.db') 
    c = conn.cursor()

    sheet_head.clear_widgets()
    sheet_box.clear_widgets() 

    if type.strip() == 'All':
        c.execute("SELECT strftime('%Y-%m-%d', date), name, type, quantity, price FROM expenses")
    else:
        c.execute("SELECT strftime('%Y-%m-%d', date), name, type, quantity, price FROM expenses WHERE type = ?", (type.strip(),))
    
    head = ['Date', 'Name', 'Type', 'Quantity', 'Price', 'Sub-Total'] 
    
    items = c.fetchall()
    conn.close()

    for i in head:
        row = MDLabel(text=i, md_bg_color='lightgray', halign='center', bold=True)
        sheet_head.add_widget(row)

    sheed_grid = SheetGrid(cols=6, items=items, items_per_page=10)
    
    sheet_box.add_widget(sheed_grid)

    self.ids.prev_exp_btn.on_press = sheed_grid.prev_page
    self.ids.next_exp_btn.on_press = sheed_grid.next_page

           
def add_exp(self):
    name = self.ids.exp_name.text_input.text
    quantity = int(self.ids.exp_qua.text_input.text)
    price = float(self.ids.exp_price.text_input.text)

    conn = sqlite3.connect('database.db') 
    c = conn.cursor()
    c.execute("INSERT INTO expenses (name, type, price, quantity) VALUES (?, ?, ?, ?)", (name, 'Unforeseen', price, quantity))
    conn.commit()
    conn.close()

    self.close_add_exp()
    self.display_exp()


def close_add_exp(self):
    self.ids.exp_name.text_input.text = ''
    self.ids.exp_qua.text_input.text = ''
    self.ids.exp_price.text_input.text = ''
    

def return_total(self):
    conn = sqlite3.connect('database.db') 
    c = conn.cursor()
    c.execute("SELECT price, quantity FROM expenses")
    items = c.fetchall()
    conn.close()
    total = 0

    for item in items:
        total += item[0] * item[1]
    
    return total