from kivy.lang import Builder
from kivymd.uix.label import MDLabel
import sqlite3


def create_table(self):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS test_table_2(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL,
        description TEXT,
        price INT NOT NULL,
        quantity INT NOT NULL   
        )
    """)

    conn.commit()
    conn.close()


def add_item(self):
    name = self.ids.item_name.text_input.text
    category = self.ids.item_cat.text_input.text
    description = self.ids.item_des.text_input.text
    price = float(self.ids.item_price.text_input.text)
    quantity = int(self.ids.item_qua.text_input.text)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO test_table_2 (name, category, description, price, quantity) VALUES (?, ?, ?, ?, ?)",
        (name, category, description, price, quantity)
    )
    conn.commit()
    conn.close()


def display_table(self):
    table = self.ids.table_box

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM test_table_2")
    items = c.fetchall()
    conn.close()

    table.cols = 6
    table.clear_widgets()

    for item in items:
        for i in item:
            label = MDLabel(text=str(i))
            table.add_widget(label)
    

