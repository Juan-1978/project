from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.divider import MDDivider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import ListProperty, NumericProperty, StringProperty, DictProperty
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
        headlines = ["Revenue", "Cost of Goods Sold", "Gross Profit", "Operating Expenses", "Operating Income", "Other Expenses", "Net Income"]
        
        head_one = self.ids.get('income_head_1')
        head_two = self.ids.get('income_head_2')
        head_three = self.ids.get('income_head_3')
        head_four = self.ids.get('income_head_4')
        head_five = self.ids.get('income_head_5')
        head_six = self.ids.get('income_head_6')
        head_seven = self.ids.get('income_head_7')
        box_one = self.ids.get('income_box_1')
        box_two = self.ids.get('income_box_2')
        box_four = self.ids.get('income_box_4')
        box_five = self.ids.get('income_box_5')
        box_six = self.ids.get('income_box_6')

        conn = sqlite3.connect('database.db') 
        c = conn.cursor()

        if head_one:
            for box in [box_one, box_two, box_four, box_five, box_six]:
                box.clear_widgets()

            index = 0
            for head in [head_one, head_two, head_three, head_four, head_five, head_six, head_seven]:
                row = MDLabel(text=headlines[index], halign='left', bold=True)
                head.add_widget(row)
                index += 1

        c.execute("SELECT name FROM incomes")
        income_names = c.fetchall()

        names = []
        for name in income_names:
            if name not in names:
                names.append(name)

        goods = {}
        for name in names:
            c.execute("SELECT quantity, sale_price FROM incomes WHERE name = ?", (name[0],))
            result = c.fetchall()
            goods[name[0]] = result

        conn.close()

        income_grid = IncomeReportGrid(items=goods, cols=1)
        box_one.add_widget(income_grid)
        

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

        for key, values in self.items.items():
            total = 0
            for quantity, price in values:
                total += quantity * price

            item = [f'{key}', f'${total:.2f}']

            row = IncomeRow(text_left='Sales of ' + item[0], text_right=item[1])
                
            self.add_widget(row) 
            grand_total += total

        print(f'Printing {grand_total}')
                    

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
            self.label = item

        if self.menu:
            self.menu.dismiss()
            self.menu = None         
    

class Headline(MDBoxLayout):
    text = StringProperty() 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint = (1, None)  
        self.height = dp(35)        
        self.md_bg_color = 'lightgray' 
        self.padding = dp(15) 

        self.label = MDLabel(bold=True)
        self.add_widget(self.label)

        self.label.bind(text=self.setter('text'))

    def on_text(self, instance, value):
        self.label.text = value


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