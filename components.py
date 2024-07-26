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
        MDTextFieldHintText:
            text: 'Password'

    MDTextField:
        mode: 'outlined'
        size_hint_x: 0.45
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
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