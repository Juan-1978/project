from kivy.config import Config
Config.set('graphics', 'width', '375')
Config.set('graphics', 'height', '650')

from kivy.core.window import Window
from kivymd.app import MDApp

from screens.login.login import LoginScreen

Window.clearcolor = (1, 1, 1, 1)

class Entrepreno(MDApp):
    def build(self):
        pass

    def on_start(self):
        if self.root:
            self.root.current = 'login'
        

if __name__ == '__main__':
    Entrepreno().run()