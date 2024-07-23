from kivy.lang import Builder
from components import KV_LOGIN, KV_REGISTER


def login_box(self):
    box = self.ids.log_box
    box.clear_widgets()
    my_widget = Builder.load_string(KV_LOGIN)
    box.add_widget(my_widget)

def register_box(self):
    box = self.ids.log_box
    box.clear_widgets()
    my_widget = Builder.load_string(KV_REGISTER)
    box.add_widget(my_widget)