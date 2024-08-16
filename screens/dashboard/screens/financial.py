from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.divider import MDDivider
import math
import sqlite3
from datetime import datetime


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
    inc_box = self.ids.inc_box
    exp_btn = self.ids.back_btn
    inc_btn = self.ids.back_inc_btn
    plus_btn = self.ids.plus_exp_btn

    financial_box.opacity = 1
    financial_box.disabled = False
    exp_box.opacity = 0
    exp_box.disabled = True
    exp_btn.opacity = 0
    exp_btn.disabled = True
    inc_box.opacity = 0
    inc_box.disabled = True
    inc_btn.opacity = 0
    inc_btn.disabled = True
    plus_btn.opacity = 0
    plus_btn.disabled = True


class SheetGrid(MDGridLayout):
    items = ListProperty()
    cols = NumericProperty(6)
    page = NumericProperty(0)
    items_per_page = NumericProperty(10)
    page_id = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_grid()

    def update_grid(self):
        self.clear_widgets()
        self.total = 0
        start = self.page * self.items_per_page
        end = start + self.items_per_page
        total = 0
        state = ExpenseState()

        for item in self.items[start:end]:
            value = item[3] * item[4]
            total += value
            updated_item = item + (value,)
            for i in updated_item:
                row = ExpensesRow(text=str(i))
                self.add_widget(row) 
            
        state.set_current_item(total)    
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
    month = self.ids.exp_month_btn.text
    year = self.ids.exp_year_btn.text
    total_exp = self.ids.total_exp

    conn = sqlite3.connect('database.db') 
    c = conn.cursor()

    sheet_head.clear_widgets()
    sheet_box.clear_widgets() 

    num = '00'

    if month == 'January':
        num = '01'
    elif month == 'February':
        num = '02'
    elif month == 'March':
        num = '03'
    elif month == 'April':
        num = '04'
    elif month == 'May':
        num = '05'
    elif month == 'June':
        num = '06'
    elif month == 'July':
        num = '07'
    elif month == 'August':
        num = '08'
    elif month == 'September':
        num = '09'
    elif month == 'October':
        num = '10'
    elif month == 'November':
        num = '11'
    elif month == 'December':
        num = '12'

    date = f'{year}-{num}'

    if type.strip() == 'All':
        c.execute("SELECT strftime('%Y-%m-%d', date), name, type, quantity, price FROM expenses WHERE strftime('%Y-%m', date) = ?", (date,))
    else:
        c.execute("SELECT strftime('%Y-%m-%d', date), name, type, quantity, price FROM expenses WHERE type = ? AND strftime('%Y-%m', date) = ?", (type.strip(), date))
    
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

    state = ExpenseState()
    total = state.get_current_item()
    total_exp.text = str(total) + '0'

           
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


def show_inc(self):
    financial_box = self.ids.financial_box
    inc_box = self.ids.inc_box
    back_btn = self.ids.back_inc_btn

    financial_box.opacity = 0
    financial_box.disabled = True
    inc_box.opacity = 1
    inc_box.disabled = False
    back_btn.opacity = 1
    back_btn.disabled = False

    self.display_inc()


def display_inc(self):
    sheet_head = self.ids.inc_sheet_head
    sheet_box = self.ids.inc_sheet_box
    month = self.ids.month_btn.text
    year = self.ids.year_btn.text
    total_inc = self.ids.total_inc

    conn = sqlite3.connect('database.db') 
    c = conn.cursor()

    sheet_head.clear_widgets()
    sheet_box.clear_widgets() 

    num = '00'

    if month == 'January':
        num = '01'
    elif month == 'February':
        num = '02'
    elif month == 'March':
        num = '03'
    elif month == 'April':
        num = '04'
    elif month == 'May':
        num = '05'
    elif month == 'June':
        num = '06'
    elif month == 'July':
        num = '07'
    elif month == 'August':
        num = '08'
    elif month == 'September':
        num = '09'
    elif month == 'October':
        num = '10'
    elif month == 'November':
        num = '11'
    elif month == 'December':
        num = '12'

    date = f'{year}-{num}'
    
    c.execute("SELECT strftime('%Y-%m-%d', date), name, quantity, sale_price FROM incomes WHERE strftime('%Y-%m', date) = ?", (date,))
    
    head = ['Date', 'Name', 'Quantity', 'Value', 'Sub-Total'] 
    
    items = c.fetchall()
    conn.close()

    for i in head:
        row = MDLabel(text=i, md_bg_color='lightgray', halign='center', bold=True)
        sheet_head.add_widget(row)

    inc_sheet_grid = IncomeSheetGrid(cols=5, items=items, items_per_page=10)
    
    sheet_box.add_widget(inc_sheet_grid)

    self.ids.prev_inc_btn.on_press = inc_sheet_grid.prev_page
    self.ids.next_inc_btn.on_press = inc_sheet_grid.next_page
    
    state = IncomeState() 
    total = state.get_current_item()
    total_inc.text = str(total) + '0'


class IncomeState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IncomeState, cls).__new__(cls)
            cls._instance.current_item = None
        return cls._instance

    def set_current_item(self, item):
        self.current_item = item

    def get_current_item(self):
        return self.current_item
    

class ExpenseState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExpenseState, cls).__new__(cls)
            cls._instance.current_item = None
        return cls._instance

    def set_current_item(self, item):
        self.current_item = item

    def get_current_item(self):
        return self.current_item


class IncomeSheetGrid(MDGridLayout):
    items = ListProperty()
    cols = NumericProperty(5)
    page = NumericProperty(0)
    items_per_page = NumericProperty(10)
    page_id = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_grid()

    def update_grid(self):
        self.clear_widgets()
        self.total = 0
        start = self.page * self.items_per_page
        end = start + self.items_per_page
        total = 0
        state = IncomeState()

        for item in self.items[start:end]:
            value = item[2] * item[3]
            total += value
            updated_item = item + (value,)
            for i in updated_item:
                row = ExpensesRow(text=str(i))
                self.add_widget(row) 

        state.set_current_item(total)
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
            label = self.parent.parent.parent.ids.inc_id
            label.text = self.page_id
        except AttributeError:
            print("Could not find the parent or label with ID 'page_id'.")

    def update_columns(self, num_cols):
        self.cols = num_cols


def current_month(self):
    current = datetime.now().date()
    month = current.month
    str_month = ''
        
    if month == 1:
        str_month = 'January'
    elif month == 2:
        str_month = 'February'
    elif month == 3:
        str_month = 'March'
    elif month == 4:
        str_month = 'April'
    elif month == 5:
        str_month = 'May'
    elif month == 6:
        str_month = 'June'
    elif month == 7:
        str_month = 'July'
    elif month == 8:
        str_month = 'August'
    elif month == 9:
        str_month = 'September'
    elif month == 10:
        str_month = 'October'
    elif month == 11:
        str_month = 'November'
    elif month == 12:
        str_month = 'December'

    return str_month
    

def current_year(self):
    current = datetime.now().date()
    year = current.year
    return year