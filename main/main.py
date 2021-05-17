from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class OperatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class OperatorApp(App):
    def build(self):
        return OperatorWindow()

oa = OperatorApp()
oa.run()