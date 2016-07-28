#!/usr/bin/python
# -*- coding: utf-8 -*-

# credits: kivy
# Still need to comment code
# Do texturing next

import kivy
from kivy.app import App
from mList import myRoot


kivy.require('1.9.1')


class MangaRoulette(App):
    def build(self):
        return myRoot


if __name__ == "__main__":
    MangaRoulette().run()
