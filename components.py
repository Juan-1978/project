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

KV_BALANCE = """
MDCard:
    size_hint: None, 0.95
    width: '500dp'
    pos_hint: {"center_x": 0.5, "center_y": 0.55}
    elevation: 4
    orientation: 'vertical'
    padding: '10dp'

    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            size_hint: 1, None
            height: '50dp'

            MDLabel:
                size_hint: 1, None
                height: '50dp'
                text: 'Please fill out all the required fields that apply to you to proceed.'
                halign: 'center'
                valign: 'middle'
        
        Widget:
            size_hint: 1, None
            height: '60dp'

        MDBoxLayout:
            orientation: 'vertical'

            BalanceInput:
                id: cash
                text: 'Cash:'
                info: 'available funds for operations'

            Widget:

            BalanceInput:
                id: receivable
                text: 'Accounts Receivable:'
                info: 'money owed to the company by customers'

            Widget:

            BalanceInput:
                id: depreciation
                text: 'Accumulated Depreciation:'
                info: 'represents the reduction in value of non-current assets over time' 

            Widget:

            BalanceInput:
                id: payable
                text: 'Accounts Payable:'
                info: 'money the company owes to suppliers' 

            Widget:

            BalanceInput:
                id: loans
                text: 'Loans:'
                info: 'borrowed funds that need to be repaid'

            Widget:

            BalanceInput:
                id: capital
                text: "Owner's Capital:"
                info: "the owner's investment in the company"
        
            Widget:

            BalanceInput:
                id: retained
                text: 'Retained Earnings:'
                info: 'profits reinvested into the business'

        Widget:
            size_hint: 1, None
            height: '20dp'

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: '50dp'
            Widget:
            MDButton:
                on_release: app.remove_form(self)
                MDButtonText:
                    text: 'Cancel'
            Widget:
                size_hint: None, None
                width: '10dp'
            MDButton:
                on_release: 
                    app.root.get_screen('balance').add_balance()
                    app.remove_form(self)
                MDButtonText:
                    text: 'Submit'
            Widget:
"""

KV_CAPITAL = """
MDCard:
    size_hint: None, None
    size: "280dp", "180dp"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 4
    orientation: 'vertical'
    padding: '10dp'

    MDLabel:
        text: 'Capital must be a valid numeric value.'
        theme_text_color: 'Secondary'
        halign: 'center'

    MDIconButton:
        icon: 'close'
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.remove_card(self)
"""

KV_NO_BALANCE = """
MDCard:
    size_hint: None, None
    size: "280dp", "180dp"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 4
    orientation: 'vertical'
    padding: '10dp'

    MDLabel:
        text: 'No Balance Sheets recorded yet. Add your first one.'
        theme_text_color: 'Secondary'
        halign: 'center'

    MDIconButton:
        icon: 'close'
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.remove_card(self)
"""

KV_NAME_ERROR = """
MDCard:
    size_hint: None, None
    size: "280dp", "180dp"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    elevation: 4
    orientation: 'vertical'
    padding: '10dp'

    MDLabel:
        text: 'You can only have one balance sheet per month.'
        theme_text_color: 'Secondary'
        halign: 'center'

    MDIconButton:
        icon: 'close'
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.remove_card(self)
"""