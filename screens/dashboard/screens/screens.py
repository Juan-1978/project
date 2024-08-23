from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDButton
from kivymd.uix.card import MDCard
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button, ButtonBehavior
from kivy.properties import StringProperty
from kivy.metrics import dp
import sqlite3
from screens.dashboard.screens.inventory import create_table, display_table, add_item, load_editing_item, save_edited_item, delete_item, show_add_card, close_add_card, close_edit_card, find_item
from screens.dashboard.screens.financial import show_exp, go_back, display_exp, add_exp, close_add_exp, display_inc, show_inc
from screens.dashboard.screens.financial_reports import show_rep


class InventoryScreen(MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'inventory'
        self.create_table()
        self.display_table()

    create_table = create_table
    display_table = display_table
    add_item = add_item
    load_editing_item = load_editing_item
    save_edited_item = save_edited_item
    delete_item = delete_item
    show_add_card = show_add_card
    close_add_card = close_add_card
    close_edit_card = close_edit_card
    find_item = find_item
    

class FinancialScreen(MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'financial'

    show_exp = show_exp
    go_back = go_back
    display_exp = display_exp
    add_exp = add_exp
    close_add_exp = close_add_exp
    display_inc = display_inc
    show_inc = show_inc
    show_rep = show_rep
    

class SalesScreen(MDFloatLayout):
    pass

class AssetsScreen(MDFloatLayout):
    pass

class AnalyticsScreen(MDFloatLayout):
    pass


class AddItem(MDBoxLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None  
        self.text_input = TextInput()     
        self.add_widgets()

    def add_widgets(self):
        self.add_widget(
            MDLabel(text=self.text)
        )


class EditItem(MDBoxLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None  
        self.text_input = MDLabel()      
        self.add_widgets()

    def add_widgets(self):
        self.add_widget(
            MDLabel(text=self.text)
        )


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


class ExpenseTypeButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = ["Unforeseen", "Operating"]
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


class DisplayButton(MDButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = [
            "All           ", "Asset        ", "Component     ", "Raw Material  ", 
            "Finished Goods", "Maintenance   ", "Packing       "
        ]
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
        parent_widget = self.parent.parent.parent
        button_text = parent_widget.ids.get('button_text')

        if self.menu:
            self.menu.dismiss()
            self.menu = None  

        button_text.text = item
        

class FinancialSection(MDCard, ButtonBehavior):
    pass


class ReportSectionButton(MDCard, ButtonBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = ["Income Statement", "Balance Sheet", "Cash Flow Statement", "Inventory Report", "Budget vs. Actual Report"]
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
        if self.text == item:
            self.text = ''
        self.text = item
        if self.menu:
            self.menu.dismiss()
            self.menu = None  


class TypeButton(MDButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = ["All         ", "Manufacturing", "Operating", "Unforeseen"]
        
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
        parent_widget = self.parent.parent.parent
        type_btn = parent_widget.ids.get('type_btn')

        if self.menu:
            self.menu.dismiss()
            self.menu = None  

        type_btn.text = item


class AddExp(MDBoxLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None  
        self.text_input = TextInput()     
        self.add_widgets()

    def add_widgets(self):
        self.add_widget(
            MDLabel(text=self.text)
        )


class MonthButton(MDButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
       
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
        parent_widget = self.parent.parent.parent
        month_btn = parent_widget.ids.get('month_btn')

        if self.menu:
            self.menu.dismiss()
            self.menu = None  

        month_btn.text = item


class ExpenseMonthButton(MDButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
       
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
        parent_widget = self.parent.parent.parent
        month_btn = parent_widget.ids.get('exp_month_btn')

        if self.menu:
            self.menu.dismiss()
            self.menu = None  

        month_btn.text = item


class IncomeYearButton(MDButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []

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
        parent_widget = self.parent.parent.parent
        year_btn = parent_widget.ids.get('year_btn') 

        if self.menu:
            self.menu.dismiss()
            self.menu = None  

        year_btn.text = item


class ExpenseYearButton(MDButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []

        conn = sqlite3.connect('database.db') 
        c = conn.cursor()
        c.execute("SELECT strftime('%Y', date) FROM expenses")
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
        parent_widget = self.parent.parent.parent
        year_btn = parent_widget.ids.get('exp_year_btn')

        if self.menu:
            self.menu.dismiss()
            self.menu = None  

        year_btn.text = item