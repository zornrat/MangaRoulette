#!/usr/bin/python
# -*- coding: utf-8 -*-

#Remember to write a help message later

import httplib
import json
import random
import urllib
import sys
import getopt
import datetime
import webbrowser
def mList(argv):
	genreList = ["Action","Adult","Adventure","Comedy","Doujinshi","Drama","Ecchi","Fantasy","Gender Bender","Harem","Historical","Horror","Josei","Martial Arts","Mature","Mecha","Mystery","One Shot","Psychological","Romance","School Life","Sci-fi","Seinen","Shoujo","Shounen","Slice of Life","Smut","Sports","Supernatural","Tragedy","Webtoons","Yaoi","Yuri"]

	try:
		opts, args = getopt.getopt(argv,"g:s:b:a:m:f:",["genre=","status=","before=","after=","more-hits=","fewer-hits="])
	except getopt.GetoptError:
		sys.stderr.write('Invalid argument usage\n')
		sys.exit(1)

	genres = []
	genreFlag = 0
	statusFlag = 0
	beforeFlag = 0
	afterFlag = 0
	mhFlag = 0
	fhFlag = 0

	for opt, arg in opts:
		if opt in ("-g","--genre"):
			if (arg not in genreList):
				sys.stdout.write(arg + " is not a valid genre. " + "Genres are: " + '["Action","Adult","Adventure","Comedy","Doujinshi","Drama","Ecchi","Fantasy","Gender Bender","Harem","Historical","Horror","Josei","Martial Arts","Mature","Mecha","Mystery","One Shot","Psychological","Romance","School Life","Sci-fi","Seinen","Shoujo","Shounen","Slice of Life","Smut","Sports","Supernatural","Tragedy","Webtoons","Yaoi","Yuri"]' + "\n")
				sys.exit(0)
			genres.append(unicode(arg))
			genreFlag = 1
		elif opt in ("-s","--status"):
			statusFlag = 1;
			status = int(arg)
			if (status != 1 and status !=2):
				sys.stderr.write('invalid status: should be 1 for "ongoing" or 2 for "completed"\n')
				sys.exit(1)
		elif opt in("-b","--before"):
			beforeFlag = 1
			beforeDate = datetime.date.fromtimestamp(float(arg))
		elif opt in("-a","--after"):
			afterFlag = 1
			afterDate = datetime.date.fromtimestamp(float(arg))
		elif opt in("-m","--more-hits"):
			mhFlag = 1
			moreHitsThan = int(arg)
		elif opt in("-f","--fewer-hits"):
			fhFlag = 1
			fewerHitsThan = int(arg)
		else:
			sys.stderr.write("Misc arg error\n")
			sys.exit(1)

	try:
		conn = httplib.HTTPSConnection("www.mangaeden.com")
		conn.request("GET", "/api/list/0/")
		r1 = conn.getresponse()
	except httplib.HTTPException:
		sys.stderr.write('Failed http connection: Mangaeden might be down or you may not have internet connectivity\n')
		sys.exit(1)

	manList = json.loads(r1.read())
	yList = []
	for entries in manList['manga']:
		addit = 1

		if (genreFlag):
			for g in genres:
				if(g not in entries['c']):
					addit = 0

		if(statusFlag):
			if(status != entries['s']):
				addit = 0

		if(beforeFlag):
			if(not entries.has_key('ld')):
				addit = 0
			else:
				if(datetime.date.fromtimestamp(entries['ld']) > beforeDate):
					addit = 0

		if(afterFlag):
			if(not entries.has_key('ld')):
				addit = 0
			else:
				if(datetime.date.fromtimestamp(entries['ld']) < afterDate):
					addit = 0

		if(mhFlag):
			if(moreHitsThan >= entries['h']):
				addit = 0

		if(fhFlag):
			if(fewerHitsThan <= entries['h']):
				addit = 0

		if (addit == 1):
			yList.append(entries['a'])

	if(yList):
		try:
			webbrowser.open_new_tab("http://www.mangaeden.com/en/en-manga/" + urllib.quote_plus(random.choice(yList)))

		except(webbrowser.Error):
			sys.stderr.write("Browser Control Error: failed to open new browser tab\n")
			sys.exit(1)

	else:
		sys.stdout.write("No Manga matching your parameters\n")
