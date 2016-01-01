#!/usr/bin/env python
# -*- coding: utf-8 -*-#
__version__ = '0.1'
__author__ = 'Georg Vogelhuber'

#--------------------------------------------------------------------------
'''dictionary that contains the correspondance between items descriptions
and methods that actually implement the specific function and panels to be
shown instead of the first main_panel
'''
SidePanel_AppMenu = {'Namen':['on_rating',None],
                     'Favoriten':['on_favorites',None],
                     'Filter':['on_filter',None],
                     }
id_AppMenu_METHOD = 0
id_AppMenu_PANEL = 1


#--------------------------------------------------------------------------
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious
from kivy.properties import StringProperty, ListProperty
from kivy.uix.label import Label

from NameProvider import NameProvider

RootApp = None

class SidePanel(BoxLayout):
    pass

class MenuItem(Button):
    def __init__(self, **kwargs):
        super(MenuItem, self).__init__( **kwargs)
        self.bind(on_press=self.menuitem_selected)

    def menuitem_selected(self, *args):
        print self.text, SidePanel_AppMenu[self.text], SidePanel_AppMenu[self.text][id_AppMenu_METHOD]
        try:
            function_to_call = SidePanel_AppMenu[self.text][id_AppMenu_METHOD]
        except:
            print 'errore di configurazione dizionario voci menu'
            return
        getattr(RootApp, function_to_call)()

class AppActionBar(ActionBar):
    pass

class ActionMenu(ActionPrevious):
    def menu(self):
        print 'ActionMenu'
        RootApp.toggle_sidepanel()

class ActionQuit(ActionButton):
    pass
    def menu(self):
        print 'App quit'
        RootApp.stop()


class MainPanel(BoxLayout):
    pass

class AppArea(FloatLayout):
    pass

class RatingView(BoxLayout):
    name_value = StringProperty()
    name_origin = StringProperty()
    gender_color = ListProperty([0,1,0,1])

    def __init__(self, **kwargs):
        super(RatingView, self).__init__( **kwargs)

        self.name_provider = NameProvider()
        self.current_name = None

        self.update_current_name()

    def update_current_name(self):
        self.current_name = self.name_provider.get_next_unrated_name()
        self.name_value = self.current_name[0]
        self.name_origin = self.current_name[1]["region"]

        if self.current_name[1]["gender"] == "m":
            self.gender_color = [0,0,1,1]
        else:
            self.gender_color = [1,0,.75,1]

    def rate_pro(self):
        self.name_provider.rate(self.current_name, 1)

        self.update_current_name()

    def rate_con(self):
        self.name_provider.rate(self.current_name, 0)

        self.update_current_name()

class FavoritesView(BoxLayout):
    def __init__(self, **kwargs):
        super(FavoritesView, self).__init__( **kwargs)
        self.displayed_names = []
        self.name_provider = NameProvider()

    def update_content(self):
        favs = self.name_provider.get_favorites()
        for name in favs:
            if name not in self.displayed_names:
                print name
                try:
                    self.ids.FavoritesBoxLayout.add_widget(Label(text=name))
                    self.displayed_names.append(name)
                except:
                    pass

class FilterView(BoxLayout):
    pass

class NavDrawer(NavigationDrawer):
    def __init__(self, **kwargs):
        super(NavDrawer, self).__init__( **kwargs)

    def close_sidepanel(self, animate=True):
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'


class AndroidApp(App):

    def build(self):

        global RootApp
        RootApp = self

        # NavigationDrawer
        self.navigationdrawer = NavDrawer()

        # SidePanel
        side_panel = SidePanel()
        self.navigationdrawer.add_widget(side_panel)

        # MainPanel
        self.main_panel = MainPanel()

        self.navigationdrawer.anim_type = 'slide_above_anim'
        self.navigationdrawer.add_widget(self.main_panel)

        return self.navigationdrawer

    def toggle_sidepanel(self):
        self.navigationdrawer.toggle_state()

    def on_rating(self):
        self._switch_main_page('Namen', RatingView)

    def on_favorites(self):
        self._switch_main_page('Favoriten', FavoritesView)

    def on_filter(self):
        self._switch_main_page('Filter',  FilterView)

    def _switch_main_page(self, key,  panel):
        self.navigationdrawer.close_sidepanel()
        if not SidePanel_AppMenu[key][id_AppMenu_PANEL]:
            SidePanel_AppMenu[key][id_AppMenu_PANEL] = panel()
        main_panel = SidePanel_AppMenu[key][id_AppMenu_PANEL]
        self.navigationdrawer.remove_widget(self.main_panel)    # FACCIO REMOVE ED ADD perchè la set_main_panel
        self.navigationdrawer.add_widget(main_panel)            # dà un'eccezione e non ho capito perchè
        self.main_panel = main_panel

if __name__ == '__main__':
    AndroidApp().run()
