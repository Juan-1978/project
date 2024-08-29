from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextFieldHelperText
from kivymd.uix.divider import MDDivider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import NumericProperty, StringProperty, DictProperty, ObjectProperty, ListProperty
from kivy.metrics import dp
import sqlite3
from kivy.app import App
from datetime import datetime
from components import KV_BALANCE, KV_CAPITAL, KV_NO_BALANCE


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
        str_income = f'${ope_income:,.2f}'
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
        str_other = f'${total_other:,.2f}'
        head_total = Headline(text_left=headlines[5], text_right=str_other)
        head_boxes[5].add_widget(head_total)

        #Net Income
        net_income = ope_income - total_other
        str_net = f'${net_income:,.2f}'
        head_total = Headline(text_left=headlines[6], text_right=str_net)
        head_boxes[6].add_widget(head_total)

        conn.close()
        

class BalanceReportScreen(Screen):
    date = StringProperty()

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.balance_rep()

    def balance_rep(self):
        headlines = ["Total Assets", "Liabilities", "Equity", "Total Liabilities and Equity"]
        head_boxes = [
            self.ids.get('balance_head_1'),
            self.ids.get('balance_head_2'),
            self.ids.get('balance_head_3'),
            self.ids.get('balance_head_4')
        ]
        sub_boxes = [
            self.ids.get('balance_sub_1'),
            self.ids.get('balance_sub_2')
        ]
        boxes = [
            self.ids.get('balance_box_1'),
            self.ids.get('balance_box_2'),
            self.ids.get('balance_box_3'),
            self.ids.get('balance_box_4')
        ]

        try:
            record = self.ids.balance_name_stmt.label.text
        except  AttributeError:
            card = Builder.load_string(KV_NO_BALANCE)
            self.add_widget(card)
            return
        
        months_to_number = {
            'January': '01', 'February': '02', 'March': '03', 'April': '04',
            'May': '05', 'June': '06', 'July': '07', 'August': '08',
            'September': '09', 'October': '10', 'November': '11', 'December': '12'
        }

        year = '0000'
        num = '00'

        if record:
            name = record.split('-')
            month = name[0]
            year = name[1]
            
            num = months_to_number.get(month, '00')

        self.date = f'{year}-{num}'
        
        conn = sqlite3.connect('database.db') 
        c = conn.cursor()

        if head_boxes:
            for head_box in head_boxes:
                head_box.clear_widgets()

            for sub_box in sub_boxes:
                sub_box.clear_widgets()

            for box in boxes:
                box.clear_widgets()

        #Current assets
        current_assets = {}
        c.execute("SELECT cash, receivable, inventory FROM balance_sheets WHERE name = ?", (self.date,))
        currents = c.fetchall()
        if currents:
            current = currents[0]
            current_assets['Cash'] = current[0]
            current_assets['Accounts receivable'] = current[1]
            current_assets['Inventory'] = current[2]

        current_grid = BalanceReportGrid(items=current_assets, cols=1)
        boxes[0].add_widget(current_grid)
        current_state = BalanceAssetsState()
        total_cur = current_state.get_current_item()
        total = f'${total_cur:,.2f}'
        head_total = Subline(text_left='Current Assets', text_right=total)
        sub_boxes[0].add_widget(head_total)

        #Non-current assets
        non_current_assets = {}
        c.execute("SELECT equipment, depreciation FROM balance_sheets WHERE name = ?", (self.date,))
        non_currents = c.fetchall()
        if non_currents:
            non_current = non_currents[0]
            non_current_assets['Machinery and Equipment'] = non_current[0]
            non_current_assets['Accumulated Depreciation'] = non_current[1]

        non_current_grid = NonCurrentAssetsGrid(items=non_current_assets, cols=1)
        boxes[1].add_widget(non_current_grid)
        non_current_state = BalanceAssetsState()
        total_non = non_current_state.get_current_item()
        total = f'${total_non:,.2f}'
        head_total = Subline(text_left='Non-Current Assets', text_right=total)
        sub_boxes[1].add_widget(head_total)

        #Total assets
        assets = total_cur + total_non
        total = f'${assets:,.2f}'
        assets_head = Headline(text_left=headlines[0], text_right=total)
        head_boxes[0].add_widget(assets_head)

        #Liabilities
        liabilities = {}
        c.execute("SELECT payable, loans FROM balance_sheets WHERE name = ?", (self.date,))
        liables = c.fetchall()
        if liables:
            liable = liables[0]
            liabilities['Accounts Payable'] = liable[0]
            liabilities['Loan(s)'] = liable[1]

        liable_grid = BalanceReportGrid(items=liabilities, cols=1)
        boxes[2].add_widget(liable_grid)
        liable_state = BalanceAssetsState()
        total_liable = liable_state.get_current_item()
        total = f'${total_liable:,.2f}'
        head_total = Headline(text_left=headlines[1], text_right=total)
        head_boxes[1].add_widget(head_total)

        #Equity
        equity = {}
        c.execute("SELECT capital, retained FROM balance_sheets WHERE name = ?", (self.date,))
        values = c.fetchall()
        if values:
            value = values[0]
            equity["Owner's Capital"] = value[0]
            equity['Retained Earnings'] = value[1]

        equity_grid = BalanceReportGrid(items=equity, cols=1)
        boxes[3].add_widget(equity_grid)
        equity_state = BalanceAssetsState()
        total_equity = equity_state.get_current_item()
        total = f'${total_equity:,.2f}'
        head_total = Headline(text_left=headlines[2], text_right=total)
        head_boxes[2].add_widget(head_total)

        #Total Liabilities and Equity
        grand_total = total_liable + total_equity
        total = f'${grand_total:,.2f}'
        head_total = Headline(text_left=headlines[3], text_right=total)
        head_boxes[3].add_widget(head_total)


    
        conn.close()

    def balance_form(self):
        card = Builder.load_string(KV_BALANCE) 
        self.add_widget(card)

        cash_box = card.ids.cash.input
        rec_box = card.ids.receivable.input
        dep_box = card.ids.depreciation.input
        pay_box = card.ids.payable.input
        loan_box = card.ids.loans.input
        cap_box = card.ids.capital.input
        ret_box = card.ids.retained.input

        balance_state = BalanceState()
        balance_state.set_current_item([cash_box, rec_box, dep_box, pay_box, loan_box, cap_box, ret_box])

    def add_balance(self):
        balance_state = BalanceState()
        balance = balance_state.get_current_item()

        cash_box = balance[0].text
        rec_box = balance[1].text
        dep_box = balance[2].text  
        pay_box = balance[3].text
        loan_box = balance[4].text
        cap_box = balance[5].text
        ret_box = balance[6].text 

        conn = sqlite3.connect('database.db') 
        c = conn.cursor()

        cash = float(cash_box) if cash_box != "" else 0.0
        rec = float(rec_box) if rec_box != "" else 0.0
        dep = float(dep_box) if dep_box != "" else 0.0
        pay = float(pay_box) if pay_box != "" else 0.0
        loan = float(loan_box) if loan_box != "" else 0.0
        cap = float(cap_box) if cap_box != "" else None
        ret = float(ret_box) if ret_box != "" else 0.0

        current = datetime.now().date()
        year = current.year
        month = current.month
        date = f'{year}-{month:02d}'

        inventory = []
        categories = ['Component', 'Raw Material', 'Finished Goods']
        for category in categories:
            if category == 'Finished Goods':
                c.execute("SELECT quantity, sale_price FROM inventory WHERE category = ? AND strftime('%Y-%m', date) = ?", (category, date))
            else:
                c.execute("SELECT quantity, price FROM inventory WHERE category = ? AND strftime('%Y-%m', date) = ?", (category, date))
            
            result = c.fetchall()
            inventory.append(result)

        total_inv = 0
        for item in inventory:
            for i in item:
                total_inv += (i[0] * i[1])   

        c.execute("SELECT quantity, price FROM inventory WHERE category = ?", ('Asset',))
        equipment = c.fetchall()
        total_equip = 0
        for equip in equipment:
            total_equip += (equip[0] * equip[1])

        if cap == None:
            cap_card = Builder.load_string(KV_CAPITAL)
            self.add_widget(cap_card)
        else:
            c.execute("INSERT INTO balance_sheets (name, cash, receivable, inventory, equipment, depreciation, payable, loans, capital, retained) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (date, cash, rec, total_inv, total_equip, dep, pay, loan, cap, ret)
            )
            conn.commit()

        conn.close()
        self.balance_rep()
        
    def delete_balance(self):
        print("Deleting balance...")


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


class BalanceReportGrid(MDGridLayout):
    items = DictProperty()
    cols = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_grid()

    def update_grid(self):
        self.clear_widgets()
        total = 0
        state = BalanceAssetsState()

        for key, value in self.items.items():
            total += value

            item = [f'{key}', f'${value:,.2f}']

            row = IncomeRow(text_left=item[0], text_right=item[1])
                
            self.add_widget(row) 

        state.set_current_item(total)

    def update_columns(self, num_cols):
        self.cols = num_cols    


class NonCurrentAssetsGrid(MDGridLayout):
    items = DictProperty()
    cols = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_grid()

    def update_grid(self):
        self.clear_widgets()
        total = 0
        state = BalanceAssetsState()

        for key, value in self.items.items():
            if key == 'Machinery and Equipment':
                total += value
                item = [f'{key}', f'${value:,.2f}']
            else:
                total -= value
                item = [f'{key}', f'-${value:,.2f}']

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
        conn.close()

        for year in years:
            i = year[0]
            if i not in self.items:
                self.items.append(i)

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
            self.label.text = item

        if self.menu:
            self.menu.dismiss()
            self.menu = None  

        box = self.parent.parent.parent.parent
        box.income_rep()       
    

class BalanceRecordsButton(MDButton):
    label = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []
        self.menu = None
        
        conn = sqlite3.connect('database.db') 
        c = conn.cursor()
        c.execute("SELECT name FROM balance_sheets ORDER BY id DESC")
        names = c.fetchall()
        conn.close()

        months =["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        for name in names:
            i = name[0]
            date = i.split('-')
            year = date[0]
            index = int(date[1]) - 1
            month = months[index]

            formatted_date = f'{month}-{year}'
            if formatted_date not in self.items:
                self.items.append(formatted_date)

        if len(self.items) > 0:
            self.label = MDButtonText(
                text = self.items[0],
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
        box.balance_rep()
              

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


class Subline(MDBoxLayout):
    text_left = StringProperty('')
    text_right = StringProperty('')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)  
        self.height = dp(35)         

        self.label = MDBoxLayout(orientation='horizontal', padding=[100, 0, 10, 0])
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
    

class BalanceState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BalanceState, cls).__new__(cls)
            cls._instance.current_item = None
        return cls._instance

    def set_current_item(self, item):
        self.current_item = item

    def get_current_item(self):
        return self.current_item
    
    
class BalanceAssetsState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BalanceAssetsState, cls).__new__(cls)
            cls._instance.current_item = None
        return cls._instance

    def set_current_item(self, item):
        self.current_item = item

    def get_current_item(self):
        return self.current_item


class BalanceInput(MDBoxLayout):
    text = StringProperty('')
    info = StringProperty('')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)  
        self.width = dp(450)
        self.height = dp(35)
        self.padding = [50, 0, 0, 0]
        self.box = MDBoxLayout(orientation='horizontal')
        self.box_info = MDBoxLayout()
        self.label = MDLabel()
        self.input = TextInput(
            hint_text='00.00',
            size_hint=(None, None),
            width=dp(150),
            height=dp(30),
            halign='right'
        )
        self.icon = MDIconButton(
            icon='information',
            on_press=self.show_info
        )

        self.box.add_widget(self.label)
        self.box.add_widget(self.input)
        self.box.add_widget(self.icon)

        self.add_widget(self.box)
        self.add_widget(self.box_info)

        self.bind(text=self.update_label_text)
        self.update_label_text(self, self.text)

    def update_label_text(self, instance, value):
        self.label.text = value

    def show_info(self, *args):
        if self.box_info.children:
            self.box_info.clear_widgets()
        else:
            info = MDTextFieldHelperText(text=self.info)
            self.box_info.add_widget(info)
        
