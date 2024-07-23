KV_LOGIN = """
FloatLayout:
    size: root.size 

    MDTextField:
        mode: 'outlined'
        size_hint_x: 0.45
        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
        MDTextFieldHintText:
            text: 'Username'

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
"""

KV_REGISTER = """
FloatLayout:
    size: root.size 

    MDTextField:
        mode: 'outlined'
        size_hint_x: 0.45
        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
        MDTextFieldHintText:
            text: 'Username'

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