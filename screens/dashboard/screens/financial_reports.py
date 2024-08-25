from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.divider import MDDivider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import NumericProperty, StringProperty, DictProperty, ObjectProperty, ListProperty
from kivy.metrics import dp
import sqlite3
from kivy.app import App


def show_rep(self):
    dashboard = self.parent.parent.parent 
    box = dashboard.ids.get('board_box')
    
    rep_btn = self.ids.rep_btn.text

    box.clear_widgets()
    
    report = None
    labels = ["Income Statement", "Balance Sheet", "Cash Flow Statement", "Inventory Report", "Budget vs. Actual Report"]

    if rep_btn == labels[0]:
        report = IncomeReportScreen()
    elif rep_btn == labels[1]:
        report = BalanceReportScreen()
    elif rep_btn == labels[2]:
        report = CashReportScreen()
    elif rep_btn == labels[3]:
        report = InventoryReportScreen()
    elif rep_btn == labels[4]:
        report = BudgetReportScreen()

    box.add_widget(report)


class IncomeReportScreen(Screen):
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.income_rep()
        
    def income_rep(self, *args):
        month = self.ids.income_month_stmt.label.text
        year = self.ids.income_year_stmt.label.text
        headlines = ["Revenue", "Cost of Goods Sold", "Gross Profit", "Operating Expenses", "Operating Income", "Other Expenses", "Net Income"]
        head_boxes = [
            self.ids.get('income_head_1'),
            self.ids.get('income_head_2'),
            self.ids.get('income_head_3'),
            self.ids.get('income_head_4'),
            self.ids.get('income_head_5'),
            self.ids.get('income_head_6'),
            self.ids.get('income_head_7')
        ]
        boxes = [
            self.ids.get('income_box_1'),
            self.ids.get('income_box_2'),
            self.ids.get('income_box_4'),
            self.ids.get('income_box_6')
        ]

        conn = sqlite3.connect('database.db') 
        c = conn.cursor()

        if head_boxes:
            for head_box in head_boxes:
                head_box.clear_widgets()

        for box in boxes:
            box.clear_widgets()

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

        #Revenue
        c.execute("SELECT name FROM incomes WHERE strftime('%Y-%m', date) = ?", (date,))
        income_names = c.fetchall()

        names = []
        for name in income_names:
            if name not in names:
                names.append(name)

        goods = {}
        for name in names:
            c.execute("SELECT quantity, sale_price FROM incomes WHERE name = ? AND strftime('%Y-%m', date) = ?", (name[0], date))
            result = c.fetchall()
            goods[name[0]] = result

        income_grid = IncomeReportGrid(items=goods, cols=1)
        boxes[0].add_widget(income_grid)
        state = IncomeReportState()
        total_income = state.get_current_item()
        total = f'${total_income:,.2f}'
        head_total = Headline(text_left=headlines[0], text_right=total)
        head_boxes[0].add_widget(head_total)

        #Cost of Goods
        c.execute("SELECT quantity, price FROM expenses WHERE type = ? AND strftime('%Y-%m', date) = ?", ('Manufacturing', date))
        manufacturing = c.fetchall()
        c.execute("SELECT quantity, price FROM expenses WHERE type = ? AND strftime('%Y-%m', date) = ?", ('Operating', date))
        operating = c.fetchall()
        
        costs = {}
        costs['Manufacturing (materials, labor)'] = manufacturing
        costs['Overhead costs (utilities)'] = operating
        
        cost_grid = CostReportGrid(items=costs, cols=1)
        boxes[1].add_widget(cost_grid)
        total_cost = state.get_current_item()
        total = f'${total_cost:,.2f}'
        head_total = Headline(text_left=headlines[1], text_right=total)
        head_boxes[1].add_widget(head_total)

        #Gross Profit
        profit = total_income - total_cost
        str_profit = f'${profit:,.2f}'
        head_total = Headline(text_left=headlines[2], text_right=str_profit)
        head_boxes[2].add_widget(head_total)

        #Operating Expenses
        type_expenses = ['Marketing', 'Salaries', 'Shipping']
        ope_expenses = {}
        for type in type_expenses:
            c.execute("SELECT quantity, price FROM expenses WHERE type = ? AND strftime('%Y-%m', date) = ?", (type, date))
            ope_expenses[type] = c.fetchall()

        ope_grid = CostReportGrid(items=ope_expenses, cols=1)
        boxes[2].add_widget(ope_grid)
        total_ope = state.get_current_item()
        str_total_ope = f'${total_ope:,.2f}'
        head_total = Headline(text_left=headlines[3], text_right=str_total_ope)
        head_boxes[3].add_widget(head_total)

        #Operating Income
        ope_income = profit - total_ope
        str_income = f'{ope_income:,.2f}'
        head_total = Headline(text_left=headlines[4], text_right=str_income)
        head_boxes[4].add_widget(head_total)

        #Other Expenses
        c.execute("SELECT name, quantity, price FROM expenses WHERE type = ? AND strftime('%Y-%m', date) = ?", ('Unforeseen', date))
        others = c.fetchall()

        other_expenses = {}
        for other in others:
            other_name = other[0] 
            other_cost = other[1] * other[2]
            if other_name in other_expenses:
                other_expenses[other_name] += other_cost
            else:
                other_expenses[other_name] = other_cost

        other_grid = OtherReportGrid(items=other_expenses, cols=1)
        boxes[3].add_widget(other_grid)
        total_other = state.get_current_item()
        str_other = f'{total_other:,.2f}'
        head_total = Headline(text_left=headlines[5], text_right=str_other)
        head_boxes[5].add_widget(head_total)

        #Net Income
        net_income = ope_income - total_other
        str_net = f'{net_income:,.2f}'
        head_total = Headline(text_left=headlines[6], text_right=str_net)
        head_boxes[6].add_widget(head_total)

        conn.close()
        

class BalanceReportScreen(Screen):
    pass


class BudgetReportScreen(Screen):
    pass


class CashReportScreen(Screen):
    pass


class InventoryReportScreen(Screen):
    pass


class IncomeReportGrid(MDGridLayout):
    items = DictProperty()
    cols = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_grid()

    def update_grid(self):
        self.clear_widgets()
        grand_total = 0
        state = IncomeReportState()

        for key, values in self.items.items():
            total = 0
            for quantity, price in values:
                total += quantity * price

            item = [f'{key}', f'${total:,.2f}']

            row = IncomeRow(text_left='Sales of ' + item[0], text_right=item[1])
                
            self.add_widget(row) 
            grand_total += total

        state.set_current_item(grand_total)

    def update_columns(self, num_cols):
        self.cols = num_cols


class CostReportGrid(MDGridLayout):
    items = DictProperty()
    cols = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_grid()

    def update_grid(self):
        self.clear_widgets()
        grand_total = 0
        state = IncomeReportState()

        for key, values in self.items.items():
            total = 0
            for quantity, price in values:
                total += quantity * price

            item = [f'{key}', f'${total:,.2f}']

            row = IncomeRow(text_left=item[0], text_right=item[1])
                
            self.add_widget(row) 
            grand_total += total

        state.set_current_item(grand_total)

    def update_columns(self, num_cols):
        self.cols = num_cols


class OtherReportGrid(MDGridLayout):
    items = DictProperty()
    cols = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_grid()

    def update_grid(self):
        self.clear_widgets()
        total = 0
        state = IncomeReportState()

        for key, value in self.items.items():
            total += value

            item = [f'{key}', f'${value:,.2f}']

            row = IncomeRow(text_left=item[0], text_right=item[1])
                
            self.add_widget(row) 

        state.set_current_item(total)

    def update_columns(self, num_cols):
        self.cols = num_cols


class IncomeReportMonthButton(MDButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.menu = None
        self.label = MDButtonText(
            text = App.get_running_app().current_month(),
            halign = 'left'
        )
        self.add_widget(self.label)
        self.on_release = self.show_menu
        
    def show_menu(self, *args):
        if not self.menu:
            menu_items = [{'text': item, 'on_release': lambda x=item: self.set_item(x)} for item in self.items]
            self.menu = MDDropdownMenu(
                caller=self,
                items=menu_items,
                width_mult=4
            )
        self.menu.open()

    def set_item(self, item):
        if self.label:
            self.label.text = item

        if self.menu:
            self.menu.dismiss()
            self.menu = None 

        box = self.parent.parent.parent.parent
        box.income_rep()


class IncomeReportYearButton(MDButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []
        self.label = MDButtonText(
            text = str(App.get_running_app().current_year()),
            halign = 'left'
        )
        self.add_widget(self.label)

        conn = sqlite3.connect('database.db') 
        c = conn.cursor()
        c.execute("SELECT strftime('%Y', date) FROM incomes")
        years = c.fetchall()
        print(f"Fetched years: {years}")
        conn.close()

        for year in years:
            i = year[0]
            if i not in self.items:
                self.items.append(i)
        print(f"Items in self.items: {self.items}")
        self.menu = None
        self.on_release = self.show_menu
        
    def show_menu(self, *args):
        if not self.menu:
            menu_items = [{'text': item, 'on_release': lambda x=item: self.set_item(x)} for item in self.items]
            self.menu = MDDropdownMenu(
                caller=self,
                items=menu_items,
                width_mult=4
            )
        self.menu.open()

    def set_item(self, item):
        if self.label:
            self.label = item

        if self.menu:
            self.menu.dismiss()
            self.menu = None  

        box = self.parent.parent.parent.parent
        box.income_rep()       
    

class Headline(MDBoxLayout):
    text_left = StringProperty('')
    text_right = StringProperty('')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)  
        self.height = dp(35)        
        self.md_bg_color = 'lightgray' 

        self.label = MDBoxLayout(orientation='horizontal', padding=[75, 0, 10, 0])
        self.label_left = MDLabel(text=self.text_left, halign='left', bold=True)
        self.label_right = MDLabel(text=self.text_right, halign='right', bold=True)
        self.label.add_widget(self.label_left)
        self.label.add_widget(self.label_right) 
        self.add_widget(self.label) 


class IncomeRow(MDBoxLayout):
    text_left = StringProperty('')
    text_right = StringProperty('')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'vertical'
        self.divider = MDDivider()
        self.label = MDBoxLayout(orientation='horizontal', padding=[100, 0, 10, 0])
        self.label_left = MDLabel(text=self.text_left, halign='left')
        self.label_right = MDLabel(text=self.text_right, halign='right')
        
        self.label.add_widget(self.label_left)
        self.label.add_widget(self.label_right)
        self.add_widget(self.divider)
        self.add_widget(self.label)


class IncomeReportState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IncomeReportState, cls).__new__(cls)
            cls._instance.current_item = None
        return cls._instance

    def set_current_item(self, item):
        self.current_item = item

    def get_current_item(self):
        return self.current_item