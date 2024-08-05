from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
import sqlite3
from screens.dashboard.screens.inventory import create_table, display_table, add_item, edit_item, delete_item, show_add_card


class InventoryScreen(MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'inventory'
        self.create_table()
        self.display_table()

    create_table = create_table
    display_table = display_table
    add_item = add_item
    edit_item = edit_item
    delete_item = delete_item
    show_add_card = show_add_card
    

class FinancialScreen(MDFloatLayout):
    pass

class SalesScreen(MDFloatLayout):
    pass

class AssetsScreen(MDFloatLayout):
    pass

class AnalyticsScreen(MDFloatLayout):
    pass

class MyNavigationAddItem(MDBoxLayout):
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
