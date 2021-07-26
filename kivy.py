# Created by TheGullibleKid at 7/27/2021
# @author: mumble-07

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput


class anchor_layout_demo(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lab = Label(
            text="Enter Name"
        )
        self.add_widget(self.lab)

        self.text_ip = TextInput()
        self.add_widget(self.text_ip)


class DemoApp(App):
    def build(self):
        return anchor_layout_demo


if __name__ == "__main__":
    DemoApp.run()
