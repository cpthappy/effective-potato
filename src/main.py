#!/usr/bin/env python
# -*- coding: utf-8 -*-#
__version__ = '0.1'
__author__ = 'Georg Vogelhuber'

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from NameProvider import NameProvider

class RatingView(Screen):
    name_value = StringProperty()
    name_origin = StringProperty()
    gender_color = ListProperty([0, 1, 0, 1])

    def __init__(self, **kwargs):
        super(RatingView, self).__init__(**kwargs)
        self.current_name = None

        self.update_current_name()

    def update_current_name(self):
        self.current_name = name_provider.get_next_unrated_name()

        if self.current_name:
            self.name_value = self.current_name[0]
            self.name_origin = self.current_name[1]["region"]

            if self.current_name[1]["gender"] == "m":
                self.gender_color = [0, 0, 1, 1]
            else:
                self.gender_color = [1, 0, .75, 1]
        else:
            self.name_value = "Keine weiteren Namen"
            self.gender_color = [0.5, 0.5, 0.5, 0.5]
            self.name_origin = ""

    def rate_pro(self):
        name_provider.rate(self.current_name, 1)

        self.update_current_name()

    def rate_con(self):
        name_provider.rate(self.current_name, 0)

        self.update_current_name()

class FavoritesView(Screen):
    favorite_names = ListProperty()

    def __init__(self, **kwargs):
        super(FavoritesView, self).__init__(**kwargs)
        self.favorite_names = name_provider.get_favorites()

class FilterView(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass


name_provider = NameProvider()
Window.clearcolor = get_color_from_hex('#ffffff')
presentation = Builder.load_file("android.kv")

class AndroidApp(App):
    icon = "res/logo.png"
    def build(self):
        return presentation

AndroidApp().run()
