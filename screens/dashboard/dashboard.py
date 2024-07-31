from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.properties import StringProperty
from helpers import board_box


class MyNavigationDrawerItem(ButtonBehavior, MDFloatLayout):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(48)        
        self.add_widgets()

    def add_widgets(self):
        self.add_widget(
            MDIcon(icon=self.icon)
        )
        self.add_widget(
            MDLabel(text=self.text)
        )

class DashboardScreen(Screen):
    def on_kv_post(self, base_widget):
        self.ids.nav_drawer.set_state('close')
        self.ids.account_drawer.set_state('close')
        board_box(self)
        
    board_box = board_box