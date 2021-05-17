from kivy.app import App
from pymongo import MongoClient, errors
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout

class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def validate_user(self):
        user = self.ids.username_field.text
        pwd = self.ids.pwd_field.text
        info = self.ids.info

        if user == '' or pwd == "":
            info.text = '[color=#FF0000] username and/or password required [/color]'
        else:
            if user == "admin" and pwd == 'admin':
                info.text = "[color=#00FF00] logged in successfully [/color]"
            else:
                info.text = '[color=#FF0000] Invalid username and/or password [/color]'

class OperatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class SigninApp(App):
    def build(self):
        return SigninWindow()

if __name__ == "__main__":
    sa = SigninApp()
    sa.run()