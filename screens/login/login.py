from kivy.uix.screenmanager import Screen
from helpers import login_box, register_box


class LoginScreen(Screen):
    def on_kv_post(self, base_widget):
        login_box(self)

    login_box = login_box
    register_box = register_box