#!/usr/bin/python
# -*- coding: utf-8 -*-

# Remember to write a help message later

import httplib
import json
import random
import urllib
import getopt
import datetime
import webbrowser
import scipy
from scipy.stats import scoreatpercentile
from kivy.uix.widget import Widget
import threading
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class RootWidget(Widget):
    genreStatus = {}

    def spin(self):

        if self.ids.startSpin.text != 'Working...':

            args = []

            for genre in self.genreStatus.keys():
                if self.genreStatus[genre] == 'down':
                    args.append("--genre")
                    args.append(genre)

            if self.ids.statusSpinner.text == 'Ongoing':
                args.append("--status")
                args.append("1")
            elif self.ids.statusSpinner.text == 'Finished':
                args.append("--status")
                args.append("2")

            if self.ids.popSpinner.text != 'Select Popularity':
                args.append("--popularity")
                args.append(self.ids.popSpinner.text)

            self.ids.startSpin.font_size = 72
            self.ids.startSpin.text = 'Working...'

            spinThread = threading.Thread(target=self.mList, args=[args])
            spinThread.start()


        return self

    def spinEnd(self, message='\0'):

        if message != '\0':
            self.ids.startSpin.font_size = 30
            self.ids.startSpin.text = message
        else:
            self.ids.startSpin.font_size = 72
            self.ids.startSpin.text = 'Spin'

        return self

    def mList(self, argv=[]):

        genreList = ["Action", "Adult", "Adventure", "Comedy", "Doujinshi", "Drama", "Ecchi", "Fantasy",
                     "Gender Bender",
                     "Harem", "Historical", "Horror", "Josei", "Martial Arts", "Mature", "Mecha", "Mystery", "One Shot",
                     "Psychological", "Romance", "School Life", "Sci-fi", "Seinen", "Shoujo", "Shounen",
                     "Slice of Life",
                     "Smut", "Sports", "Supernatural", "Tragedy", "Webtoons", "Yaoi", "Yuri"]

        try:
            opts, args = getopt.getopt(argv[0:], "g:s:b:a:p:",
                                       ["genre=", "status=", "before=", "after=", "popularity="])
        except:
            raise Exception('Invalid argument usage\n')

        genres = []
        genreFlag = 0
        statusFlag = 0
        beforeFlag = 0
        afterFlag = 0
        popFlag = 0
        popSetting = ''

        for opt, arg in opts:
            if opt in ("-g", "--genre"):
                if arg not in genreList:
                    raise Exception(
                        arg + " is not a valid genre. " + "Genres are: " + '["Action","Adult","Adventure","Comedy","Doujinshi","Drama","Ecchi","Fantasy","Gender Bender","Harem","Historical","Horror","Josei","Martial Arts","Mature","Mecha","Mystery","One Shot","Psychological","Romance","School Life","Sci-fi","Seinen","Shoujo","Shounen","Slice of Life","Smut","Sports","Supernatural","Tragedy","Webtoons","Yaoi","Yuri"]' + "\n")
                genres.append(unicode(arg))
                genreFlag = 1
            elif opt in ("-s", "--status"):
                statusFlag = 1
                status = int(arg)
                if status != 1 and status != 2:
                    raise Exception('invalid status: should be 1 for "ongoing" or 2 for "completed"\n')
            elif opt in ("-b", "--before"):
                beforeFlag = 1
                beforeDate = datetime.date.fromtimestamp(float(arg))
            elif opt in ("-a", "--after"):
                afterFlag = 1
                afterDate = datetime.date.fromtimestamp(float(arg))
            elif opt in ("-p", "--popularity"):
                popFlag = 1
                if arg not in ("Low", "Medium", "High"):
                    raise Exception("Must select 'low', 'medium', or 'high' for popularity option.\n")
                else:
                    popSetting = arg
            else:
                raise Exception("Misc arg error\n")

        try:
            conn = httplib.HTTPSConnection("www.mangaeden.com")
            conn.request("GET", "/api/list/0/")
            r1 = conn.getresponse()
        except:
            exceptionPopup = Popup(title='Connectivity Error:', size_hint=[0.75,0.75],
                                   content= Label(text='Cannot connect to the internet\nor MangaEden may be down.', font_size = 40))
            self.spinEnd()
            exceptionPopup.open()
            return

        manList = json.loads(r1.read())
        yList = []

        if popFlag == 1:
            popArray = []
            for m in manList['manga']:
                popArray.append(int(m['h']))
            firstThridPercentile = scipy.stats.scoreatpercentile(popArray, 33)
            secondThirdPercentile = scipy.stats.scoreatpercentile(popArray, 67)

        for entries in manList['manga']:
            addit = 1

            if genreFlag:
                for g in genres:
                    if g not in entries['c']:
                        addit = 0

            if statusFlag:
                if status != entries['s']:
                    addit = 0

            if beforeFlag:
                if not entries.has_key('ld'):
                    addit = 0
                else:
                    if datetime.date.fromtimestamp(entries['ld']) > beforeDate:
                        addit = 0

            if afterFlag:
                if not entries.has_key('ld'):
                    addit = 0
                else:
                    if datetime.date.fromtimestamp(entries['ld']) < afterDate:
                        addit = 0

            if popFlag:
                if popSetting == "Low":
                    if entries['h'] > firstThridPercentile:
                        addit = 0
                elif popSetting == "Medium":
                    if entries['h'] <= firstThridPercentile or entries['h'] >= secondThirdPercentile:
                        addit = 0
                elif popSetting == "High":
                    if entries['h'] < secondThirdPercentile:
                        addit = 0

            if addit == 1:
                yList.append(entries['a'])

        if yList:
            try:
                webbrowser.open_new_tab(
                    "http://www.mangaeden.com/en/en-manga/" + urllib.quote_plus(random.choice(yList)))
                self.spinEnd()

            except:
                exceptionPopup = Popup(title='Browser Open Error:', size_hint=[0.75, 0.75],
                                       content=Label(text='Failed to open new browser tab.',
                                                     font_size=40))
                self.spinEnd()
                exceptionPopup.open()
                return

        else:
            self.spinEnd("No Results. Try again?")


myRoot = Builder.load_file('RootWidget.kv')
