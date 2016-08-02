#!/usr/bin/python
# -*- coding: utf-8 -*-

# credits: kivy
# Still need to comment code
# Do texturing next

from kivy import require
from kivy.app import App

from mList import myRoot

require('1.9.1')


class MangaRoulette(App):
    def build(self):
        return myRoot

    def on_pause(self):
        return True


if __name__ == "__main__":
    MangaRoulette().run()
