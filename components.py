KV_LOGIN = """
FloatLayout:
    size: root.size 

    MDTextField:
        mode: 'outlined'
        size_hint_x: 0.45
        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
        MDTextFieldHintText:
            text: 'Email'

    MDTextField:
        mode: 'outlined'
        size_hint_x: 0.45
        pos_hint: {'center_x': 0.5, 'center_y': 0.625}
        password: True
        MDTextFieldHintText:
            text: 'Password'

    MDButton:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        radius: [5, 5, 5, 5]
        MDButtonText:
            text: 'Log In'

    Button:
        text: 'Forgot your password?'
        color: 'blue'
        size_hint: 0.45, None
        height: '50dp'
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
        background_normal: ''
        background_down: ''
        on_release: 
            app.root.current = 'reset'
"""

KV_REGISTER = """
FloatLayout:
    size: root.size 

    MDTextField:
        mode: 'outlined'
        size_hint_x: 0.45
        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
        MDTextFieldHintText:
            text: 'Email'

    MDTextField:
        mode: 'outlined'
        size_hint_x: 0.45
        pos_hint: {'center_x': 0.5, 'center_y': 0.625}
        password: True
        MDTextFieldHintText:
            text: 'Password'

    MDTextField:
        mode: 'outlined'
        size_hint_x: 0.45
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        password: True
        MDTextFieldHintText:
            text: 'Password'

    MDButton:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.375}
        radius: [5, 5, 5, 5]
        MDButtonText:
            text: 'Register'
"""

KV_RESET = """
MDFloatLayout:
    width: '375'
    size_hint_y: 0.3
    pos_hint: {'center_x': 0.5, 'center_y': 0.45}
    md_bg_color: 'white'

    MDTextField:
        mode: 'outlined'
        size_hint_x: 0.75
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        MDTextFieldHintText:
            text: 'john@example.com'

    MDFloatLayout:
        size_hint: 0.75, 0.15
        pos_hint: {'center_x': 0.5, 'center_y': 0.275}

        MDButton:
            style: 'tonal'
            radius: [5, 5, 5, 5]
            pos_hint: {'center_x': 0.355, 'center_y': 0.38}
            on_release:
                app.root.current = 'login'
                app.root.get_screen('reset').reset_form()
            MDButtonText:
                text: 'Back'

        MDButton:
            style: 'filled'
            pos_hint: {'center_x': 0.645, 'center_y': 0.38}
            radius: [5, 5, 5, 5]
            on_release: 
                app.root.get_screen('reset').send_text()
            MDButtonText:
                text: 'Send'
"""

KV_TEXT = """
MDFloatLayout:
    width: '375'
    size_hint_y: 0.3
    pos_hint: {'center_x': 0.5, 'center_y': 0.45}
    md_bg_color: 'white'

    MDCard:
        style: 'outlined'
        size_hint: 0.8, 0.5
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        radius: [10, 10, 10, 10]
        padding: [10, 10, 10, 10] 

        MDLabel:
            text: 'If your address is present in our database, you will receive a reset email within a few moments'
            color: 'green'
            adaptative_size: True
            font_size: '14sp'
            halign: 'center'

    MDFloatLayout:
        size_hint: 0.75, 0.15
        pos_hint: {'center_x': 0.5, 'center_y': 0.275}

        MDButton:
            style: 'tonal'
            radius: [5, 5, 5, 5]
            pos_hint: {'center_x': 0.5, 'center_y': 0.38}
            on_release:
                app.root.current = 'login'
                app.root.get_screen('reset').reset_form()
            MDButtonText:
                text: 'Back'
"""

KV_BOARD = """
Label:
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    text: 'Dashboard'
    color: 'black'
"""

ADD_ONE = """
MDCard:
    size_hint: 0.9, 0.35
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    padding: '10dp'
    spacing: '10dp'
    orientation: 'horizontal'

    MDBoxLayout:
        orientation: 'vertical'
        size_hint: 1, 0.25

    MDBoxLaout:
        orientation: 'vertical' 
        size_hint: 1, 0.50
        md_bg_color: 'red'  
        
    Button:
        text: 'Submit'
"""

KV_NO_INPUT = """
MDCard:
    size_hint: None, None
    size: "280dp", "180dp"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 4
    orientation: 'vertical'
    padding: '10dp'

    MDLabel:
        text: 'Please enter a name.'
        theme_text_color: 'Secondary'
        halign: 'center'

    MDIconButton:
        icon: 'close'
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.remove_card(self)
"""

KV_NOT_FOUND = """
MDCard:
    size_hint: None, None
    size: "280dp", "180dp"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 4
    orientation: 'vertical'
    padding: '10dp'

    MDLabel:
        text: 'Item not found.'
        theme_text_color: 'Secondary'
        halign: 'center'

    MDIconButton:
        icon: 'close'
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.remove_card(self)
"""

KV_EXIST = """
MDCard:
    size_hint: None, None
    size: "280dp", "180dp"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 4
    orientation: 'vertical'
    padding: '10dp'

    MDLabel:
        text: 'That name already exists.'
        theme_text_color: 'Secondary'
        halign: 'center'

    MDIconButton:
        icon: 'close'
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.remove_card(self)
"""

KV_NOT_ENOUGH = """
MDCard:
    size_hint: None, None
    size: "280dp", "180dp"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 4
    orientation: 'vertical'
    padding: '10dp'

    MDLabel:
        text: 'Not enough items in stock to process this order.'
        theme_text_color: 'Secondary'
        halign: 'center'

    MDIconButton:
        icon: 'close'
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.remove_card(self)
"""

KV_FILLOUT = """
MDCard:
    size_hint: None, None
    size: "280dp", "180dp"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 4
    orientation: 'vertical'
    padding: '10dp'

    MDLabel:
        text: 'All fields must be filled out.'
        theme_text_color: 'Secondary'
        halign: 'center'

    MDIconButton:
        icon: 'close'
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.remove_card(self)
"""

KV_FORMAT = """
MDCard:
    size_hint: None, None
    size: "280dp", "180dp"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 4
    orientation: 'vertical'
    padding: '10dp'

    MDLabel:
        text: 'All fields must be filled out in a proper format.'
        theme_text_color: 'Secondary'
        halign: 'center'

    MDIconButton:
        icon: 'close'
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.remove_card(self)
"""

KV_INCOME_STMT = """
MDBoxLayout:
    id: income_head
    size_hint: 1, 0.15
    padding: '35dp'
    spacing: '10dp'
    orientation: 'horizontal'

    MDLabel:
        text: 'Profit and Loss Statement'
        halign: 'center'
        valign: 'middle'

    MDLabel:
        text: 'Month:'
        halign: 'right'

    IncomeMonthButton:
        id: income_month_stmt
        MDButtonText:
            id: income_month_text
            text: app.current_month()
            halign: 'left'
            #on_text: root.display_exp()
        MDButtonIcon:
            icon: 'menu'
            style: "standard"
            theme_font_size: "Custom"
            font_size: "16sp"
            radius: [self.height / 2, ]
            size_hint: None, None
            size: "30dp", "30dp"

        MDLabel:
            text: 'Year:'
            halign: 'right'

        IncomeYearButton:
            MDButtonText:
                id: income_year_stmt
                text: str(app.current_year())
                halign: 'left'
                #on_text: root.display_exp()
            MDButtonIcon:
                icon: 'menu'
                style: "standard"
                theme_font_size: "Custom"
                font_size: "16sp"
                radius: [self.height / 2, ]
                size_hint: None, None
                size: "30dp", "30dp"
"""

KV_REP_BOX = """
MDFloatLayout:
    id: financial_report_box

    MDBoxLayout:
        id: report_sections
        size: root.size
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        orientation: 'horizontal'
        spacing: '25dp'
        padding: '25dp'

        ReportSection:
            id: inc_stmt
            on_press: root.stmt()
            MDLabel:
                text: 'Profit and Loss Statement'
                halign: 'center'
                font_size: '24sp'
                bold: True

        ReportSection:
            id: balance_stmt
            #on_press: root.show_exp()
            MDLabel:
                text: 'Balance Sheet'
                halign: 'center'
                font_size: '24sp'
                bold: True

        ReportSection:
            id: cash_stmt
            #on_press: root.show_exp()
            MDLabel:
                text: 'Cash Flow Statement'
                halign: 'center'
                font_size: '24sp'
                bold: True

        ReportSection:
            id: inventory_stmt
            #on_press: root.show_exp()
            MDLabel:
                text: 'Inventory Report'
                halign: 'center'
                font_size: '24sp'
                bold: True

        ReportSection:
            id: budget_stmt
            #on_press: root.show_exp()
            MDLabel:
                text: 'Budget vs. Actual Report'
                halign: 'center'
                font_size: '24sp'
                bold: True

    MDBoxLayout:
        id: test 
        opacity: 0
        disabled: True
        md_bg_color: 'red'
"""