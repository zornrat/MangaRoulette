#!/usr/bin/python
# -*- coding: utf-8 -*-

#credits: kivy

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty
from kivy.config import Config

class GenToggle(ToggleButton):
    pass

class RootWidget(Widget):
    pass

class DateTimeSelect(Widget):
    pass

class mangaRoulette(App):
    def build(self):
        Config.set('graphics','height','600')
        Config.set('graphics', 'width','800')
        Config.set('graphics','minimum_height','600')
        Config.set('graphics', 'minimum_width','800')
        return RootWidget()

mangaRoulette().run()
