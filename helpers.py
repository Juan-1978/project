from kivy.lang import Builder
from components import KV_LOGIN, KV_REGISTER, KV_RESET, KV_TEXT, KV_BOARD, ADD_ONE
from screens.dashboard.screens.screens import InventoryScreen, FinancialScreen, SalesScreen, AssetsScreen, AnalyticsScreen


def login_box(self):
    box = self.ids.log_box
    box.clear_widgets()
    my_widget = Builder.load_string(KV_LOGIN)
    box.add_widget(my_widget)

def sign_out(self):
    self.root.current = 'login'

def register_box(self):
    box = self.ids.log_box
    box.clear_widgets()
    my_widget = Builder.load_string(KV_REGISTER)
    box.add_widget(my_widget)

def reset_form(self):
    box = self.ids.reset_box
    box.clear_widgets()
    my_widget = Builder.load_string(KV_RESET)
    box.add_widget(my_widget)

def send_text(self):
    box = self.ids.reset_box
    box.clear_widgets()
    my_widget = Builder.load_string(KV_TEXT)
    box.add_widget(my_widget)
    
def board_box(self):
    box = self.ids.board_box
    box.clear_widgets()
    my_widget = Builder.load_string(KV_BOARD)
    box.add_widget(my_widget)
    nav_drawer = self.ids.get('nav_drawer')
    nav_drawer.set_state('close')

def on_drawer_press(self, screen_name):
    dashboard = self.root.get_screen('dashboard')
    box = dashboard.ids.get('board_box')
    
    box.clear_widgets()

    if screen_name == 'inventory':
        screen = InventoryScreen()
    elif screen_name == 'financial':
        screen = FinancialScreen()
    elif screen_name == 'sales':
        screen = SalesScreen()
    elif screen_name == 'assets':
        screen = AssetsScreen()
    elif screen_name == 'analytics':
        screen = AnalyticsScreen()

    box.add_widget(screen)
    nav_drawer = dashboard.ids.get('nav_drawer')
    nav_drawer.set_state('close')
    

def remove_card(self, button_instance):
    card = button_instance.parent  
    parent_layout = card.parent  
    if parent_layout:
        parent_layout.remove_widget(card)