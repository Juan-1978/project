from kivy.uix.screenmanager import Screen
from helpers import reset_form, send_text


class ResetScreen(Screen):
    def on_kv_post(self, base_widget):
        reset_form(self)

    reset_form = reset_form
    send_text = send_text
