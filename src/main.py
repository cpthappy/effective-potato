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
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListItemButton, ListItemLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.rst import RstDocument

from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from kivy.garden import iconfonts

from NameProvider import NameProvider, make_lang_key

LANGS = [u'Friesisch',
u'Lateinisch',
u'Etruskisch',
u'Französisch',
u'Italienisch',
u'Englisch',
u'Irisch',
u'Hebräisch',
u'Keltisch',
u'Persisch',
u'Arabisch',
u'Unbekannt',
u'Nordisch',
u'Deutsch',
u'Walisisch',
u'Slawisch',
u'Griechisch'
]



class RatingView(Screen):
    name_value = StringProperty()
    name_info = StringProperty()

    gender_color = ListProperty((0.467, 0.286, 1, 0.75))

    def __init__(self, **kwargs):
        super(RatingView, self).__init__(**kwargs)
        self.current_name = None
        self.remaining_names = 0
        self.update_current_name()

    def update_current_name(self):
        try:
            config = AndroidApp.get_running_app().config
            gender = config.getdefault("Filter", "gender", "").lower()
            starts_with = config.getdefault("Filter", "starts_with", "").lower()
            ends_with = config.getdefault("Filter", "ends_with", "").lower()
            min_len = config.getdefault("Filter", "min_len", 1).lower()
            max_len = config.getdefault("Filter", "max_len", 20).lower()
            langs = {make_lang_key(x) :config.getdefault("Sprache", make_lang_key(x), u'1') for x in LANGS}
        except:
            gender = "Beide"
            starts_with = ""
            ends_with = ""
            min_len = 1
            max_len = 20
            langs = {make_lang_key(x) :u'1' for x in LANGS}

        self.current_name, self.remaining_names = name_provider.get_next_unrated_name(gender,
                                                                starts_with,
                                                                ends_with,
                                                                min_len,
                                                                max_len,
                                                                langs)

        if self.current_name:
            self.name_value = self.current_name[0]
            self.name_info = name_provider.get_rst(*self.current_name)

            if self.current_name[1]["gender"].startswith("m"):
                self.gender_color = (0.235, 0.451, 1, 0.75)
            else:
                self.gender_color = (0.847, 0.235, 1, 0.75)
        else:
            self.name_value = iconfonts.icon("flaticon-prohibition23")
            self.gender_color = (0.467, 0.286, 1, 0.5)
            self.name_info = "Zur Anzeige weiterer Namen, Filtereinstellungen ändern oder Bewertungen löschen."

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

    def remove(self, an_obj):
        current_name = name_provider.get_by_name(an_obj.id)
        del current_name[1]['rating']
        name_provider.rate(current_name, 0)
        self.update()

    def info(sefl, an_obj):
        name = name_provider.get_by_name(an_obj.id.split('_')[-1])
        if name[1]["gender"].startswith("m"):
            box_color = (0.235, 0.451, 1, 0.75)
        else:
            box_color = (0.847, 0.235, 1, 0.75)

        box = BoxLayout(orientation='vertical')
        text = name_provider.get_rst(name[0], name[1])
        document = RstDocument(text=text, size_hint=(1.,0.9))
        close_button = Button(text=u"Zurück",
        markup=True, size_hint=(1., 0.1),
        background_color=(0.467, 0.286, 1, 0.75))
        box.add_widget(document)
        box.add_widget(close_button)

        popup = Popup(title=name[0],
                    content=box,
                    auto_dismiss = False,
                    title_color = box_color,
                    title_size = '30sp',
                    title_align = 'center',
                    separator_color=(0.467, 0.286, 1, 0.75))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def args_converter(self, row_index, an_obj):
        if an_obj[1]["gender"].startswith("m"):
            box_color = (0.235, 0.451, 1, 0.75)
        else:
            box_color = (0.847, 0.235, 1, 0.75)
        return {'text': an_obj[0],
                 'size_hint_y': None,
                 'height': 60,
                 'cls_dicts': [

                                {'cls': ListItemButton,
                                'kwargs': {'text': an_obj[0],
                                            'color' : box_color,
                                            'font_size': '30sp',
                                            'height': 50,
                                            'size_hint_x': 1,
                                            'id': 'info_' + an_obj[0],
                                            'background_normal': "",
                                             'on_press': self.info,
                                             'deselected_color': [1,1,1,1]}},

                                {'cls': ListItemButton,
                                 'kwargs': {'text': iconfonts.icon('flaticon-rounded61'),
                                 'deselected_color': [1,1,1,1],
                                 'color': (1, 0.678, 0.384, 0.75),
                                 'background_normal': "",
                                 #'background_down': "",
                                 'markup':True,
                                 'id': an_obj[0],
                                 'size_hint_x': 0.25,
                                 'font_size': '30sp',
                                 'on_press': self.remove,
                                 'halign': 'left'}}
                               ]}


class ScreenManagement(ScreenManager):
    pass


iconfonts.register('default_font', 'flaticon.ttf', 'flaticon.fontd')
name_provider = NameProvider()
Window.clearcolor = get_color_from_hex('#ffffff')
presentation = Builder.load_file("android.kv")

class AndroidApp(App):
    icon = "res/sparrow.png"
    use_kivy_settings  =  False

    def build(self):
        self.mainwidget = presentation
        self.update_after_config()
        return self.mainwidget

    def on_pause(self):
        return True

    def update_after_config(self, *args, **kwargs):
        self.mainwidget.get_screen('rating').update_current_name()

    def build_config(self, config):
        config.setdefaults('Filter', { 'gender': "Beide",
                                        'starts_with': "",
                                        'ends_with': "",
                                        'min_len': 1,
                                        'max_len': 20 })
        config.setdefaults('Sprache', {make_lang_key(l) :1 for l in LANGS})

    def build_settings(self, settings):
        settings.add_json_panel("Filter Einstellungen", self.config, data = """
            [
                {"type": "options", "title": "Geschlecht", "section": "Filter", "key": "gender", "options": ["Beide", "männlich", "weiblich"]},
                {"type": "string", "title": "Anfang", "section": "Filter", "key": "starts_with"},
                {"type": "string", "title": "Ende", "section": "Filter", "key": "ends_with"},
                {"type": "numeric", "title": "Minimale Länge", "section": "Filter", "key": "min_len"},
                {"type": "numeric", "title": "Maximale Länge", "section": "Filter", "key": "max_len"}
            ]
        """
        )

        lang_json=[]
        for language in sorted(LANGS):
            lang_json.append("""{"type": "bool", "title": "%s", "section": "Sprache", "key": "%s"}""" %
            (language, make_lang_key(language) ))

        settings.add_json_panel("Filter für Herkunft", self.config, data= "[%s]" % (','.join(lang_json)))

        settings.bind(on_config_change=self.update_after_config)

AndroidApp().run()
