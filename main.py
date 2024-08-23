from kivy.config import Config
#Config.set('graphics', 'width', '375')
#Config.set('graphics', 'height', '650')

from kivy.core.window import Window 
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationItemLabel

from screens.login.login import LoginScreen
from screens.login.reset import ResetScreen
from screens.dashboard.dashboard import DashboardScreen 
from screens.dashboard.screens.screens import InventoryScreen, FinancialScreen, SalesScreen, AssetsScreen, AnalyticsScreen
from screens.dashboard.screens.financial_reports import IncomeReportScreen

from helpers import on_drawer_press, sign_out, remove_card, current_month, current_year

Window.clearcolor = (1, 1, 1, 1)


class Entrepreno(MDApp):
    def build(self): 
        self.theme_cls.primary_palette = "Cadetblue"
        self.theme_cls.accent_palette = "Orangered"
        self.theme_cls.theme_style = "Light"  

        self.theme_cls.primary_color = [0.1, 0.5, 0.7, 1]

        return Builder.load_file('main.kv') 
    
    on_drawer_press = on_drawer_press
    sign_out = sign_out
    remove_card = remove_card
    current_year = current_year
    current_month = current_month
    
    def on_start(self):
        if self.root:
            self.root.current = 'dashboard'
     

if __name__ == '__main__':
    Entrepreno().run()

