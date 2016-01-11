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

from kivy.garden import iconfonts

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
        try:
            config = AndroidApp.get_running_app().config
            gender = config.getdefault("Filter", "gender", "").lower()
            starts_with = config.getdefault("Filter", "starts_with", "").lower()
            ends_with = config.getdefault("Filter", "ends_with", "").lower()
            min_len = config.getdefault("Filter", "min_len", 1).lower()
            max_len = config.getdefault("Filter", "max_len", 20).lower()
        except:
            gender = "Beide"
            starts_with = ""
            ends_with = ""
            min_len = 1
            max_len = 20
            print "FEHLER"
        self.current_name = name_provider.get_next_unrated_name(gender,
                                                                starts_with,
                                                                ends_with,
                                                                min_len,
                                                                max_len)

        if self.current_name:
            #self.rate_pro_btn.enabled = True
            #self.rate_con_btn.enabled = True
            self.name_value = self.current_name[0]
            self.name_origin = self.current_name[1]["region"]

            if self.current_name[1]["gender"] == "m":
                self.gender_color = [0, 0, 1, 1]
            else:
                self.gender_color = [1, 0, .75, 1]
        else:
            #self.rate_pro_btn.enabled = False
            #self.rate_con_btn.enabled = False
            self.name_value = "Keine weiteren\nNamen"
            self.gender_color = [0.5, 0.5, 0.5, 0.5]
            self.name_origin = "Zur Anzeige weiterer Namen\nFilter oder Bewertungen\nlöschen."

    def rate_pro(self):
        try:
            name_provider.rate(self.current_name, 1)
            self.update_current_name()
        except TypeError:
            pass

    def rate_con(self):
        try:
            name_provider.rate(self.current_name, 0)
            self.update_current_name()
        except TypeError:
            pass

class FavoritesView(Screen):
    favorite_names = ListProperty()

    def __init__(self, **kwargs):
        super(FavoritesView, self).__init__(**kwargs)
        self.favorite_names = name_provider.get_favorites()

    def update(self):
        self.favorite_names = name_provider.get_favorites()
        self.ids.favorite_list._trigger_reset_populate()

    def args_converter(self, row_index, an_obj):
        print an_obj
        if an_obj[1]["gender"] == "m":
            box_color = [0, 0, 1, 1]
        else:
            box_color = [1, 0, .75, 1]
        return {'text': an_obj[0],
                'size_hint_y': None,
                'font_size': '30sp',
                'height': 50,
                'color': box_color,
                'deselected_color': [1,1,1,1],
                'selected_color': [0.5, 0.5, 0.5, 0.5],
                'background_normal': ""}

class FilterView(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass


iconfonts.register('default_font', 'flaticon.ttf', 'flaticon.fontd')
name_provider = NameProvider()
Window.clearcolor = get_color_from_hex('#ffffff')
presentation = Builder.load_file("android.kv")

class AndroidApp(App):
    icon = "res/logo.png"
    use_kivy_settings  =  False

    def build(self):
        return presentation

    def build_config(self, config):
        config.setdefaults('Filter', { 'gender': "Beide",
                                        'starts_with': "",
                                        'ends_with': "",
                                        'min_len': 1,
                                        'max_len': 20 })
    def build_settings(self, settings):
        settings.add_json_panel("Filter Einstellungen", self.config, data = """
            [
                {"type": "options", "title": "Geschlecht", "section": "Filter", "key": "gender", "options": ["Beide", "Junge", "Mädchen"]},
                {"type": "string", "title": "Anfang", "section": "Filter", "key": "starts_with"},
                {"type": "string", "title": "Ende", "section": "Filter", "key": "ends_with"},
                {"type": "numeric", "title": "Minimale Länge", "section": "Filter", "key": "min_len"},
                {"type": "numeric", "title": "Maximale Länge", "section": "Filter", "key": "max_len"}
            ]
        """
        )

AndroidApp().run()
