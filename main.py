#!/usr/bin/python
# -*- coding: utf-8 -*-

# credits: kivy
# Still need to comment code
# Do texturing next

import kivy
from kivy.app import App
from kivy.config import Config
from mList import myRoot

kivy.require('1.9.1')


class MangaRoulette(App):
    def build(self):
        Config.set('graphics', 'height', '600')
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'minimum_height', '600')
        Config.set('graphics', 'minimum_width', '800')
        return myRoot


if __name__ == "__main__":
    MangaRoulette().run()
