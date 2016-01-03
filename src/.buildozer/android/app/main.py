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
from NameProvider import NameProvider

class RatingView(Screen):
    name_value = StringProperty()
    name_origin = StringProperty()
    gender_color = ListProperty([0, 1, 0, 1])

    def __init__(self, **kwargs):
        super(RatingView, self).__init__(**kwargs)
        self.name_provider = NameProvider()
        self.current_name = None

        self.update_current_name()

    def update_current_name(self):
        self.current_name = self.name_provider.get_next_unrated_name()
        self.name_value = self.current_name[0]
        self.name_origin = self.current_name[1]["region"]

        if self.current_name[1]["gender"] == "m":
            self.gender_color = [0, 0, 1, 1]
        else:
            self.gender_color = [1, 0, .75, 1]

    def rate_pro(self):
        self.name_provider.rate(self.current_name, 1)

        self.update_current_name()

    def rate_con(self):
        self.name_provider.rate(self.current_name, 0)

        self.update_current_name()

class FavoritesView(Screen):
    favorite_names = ListProperty()

    def __init__(self, **kwargs):
        super(FavoritesView, self).__init__(**kwargs)
        self.name_provider = NameProvider(callback=self.update)
        self.favorite_names = self.name_provider.get_favorites()

    def update(self):
        self.favorite_names = self.name_provider.get_favorites()
        self.ids.favorite_list.data = self.favorite_names
        self.ids.favorite_list.populate()


class FilterView(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("android.kv")

class AndroidApp(App):
    def build(self):
        return presentation

AndroidApp().run()
