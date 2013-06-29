#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Christopher Kaster (@Kasoki)
# 
# This file is part of Maestro <https://github.com/Kasoki/Maestro>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import subprocess
import sys
import os
import hashlib
import Alfred
import romkan

handler = Alfred.Handler(sys.argv, use_no_query_string=False)

anything_matched = False
playlist_name = ""

# IMPORTANT: If you change this value you also need to change it in the workflow!
recache_identifier = ".disallow-recache"

# for debug purpose
#handler.query = "hito"

user_home = os.path.expanduser("~")
artwork_cache_path = os.path.join(user_home, ".maestro-cache/")

if not os.path.exists(artwork_cache_path):
	os.makedirs(artwork_cache_path)

def get_artwork(track_name):
	file_name = hashlib.md5(track_name).hexdigest()
	items = os.listdir(artwork_cache_path)

	if not os.path.exists(recache_identifier):
		sprocess = subprocess.Popen(["osascript", "get_artwork.scpt", track_name, artwork_cache_path, file_name], stdout=subprocess.PIPE)

	for item in items:
		if file_name in item:
			return os.path.join(artwork_cache_path, item)

	return "no_album_art.jpg"

def disallow_recache():
	os.system("touch %s" % recache_identifier)

try:
	# get playlist name
	sprocess = subprocess.Popen(["osascript", "get_playlist_name.scpt"], stdout=subprocess.PIPE)

	playlist_name = sprocess.stdout.read()

	# remove empty line
	playlist_name = playlist_name[:-1]

	# get all playlist tracks
	sprocess = subprocess.Popen(["osascript", "get_playlist_tracks.scpt"], stdout=subprocess.PIPE)

	playlist_track_infos_raw = sprocess.stdout.read()

	# remove empty line
	playlist_track_infos_raw = playlist_track_infos_raw[:-1]

	playlist_track_infos = playlist_track_infos_raw.split('\n')

	playlist_tracks = []

	for raw_info in playlist_track_infos:
		info = raw_info.split('!MAESTRO!')
		track_artist = info[0]
		track_name = info[1]

		if "'" in track_name:
			track_name = track_name.replace("'", "`")

		playlist_tracks.append({"artist": track_artist, "name": track_name})

	

	for track in playlist_tracks:
		match_in_name = handler.query.lower() in track["name"].lower()
		match_in_artist = handler.query.lower() in track["artist"].lower()
		match_in_name_kana = handler.query.lower() in romkan.to_roma(unicode(track["name"], "utf-8"))
		match_in_artist_kana = handler.query.lower() in romkan.to_roma(unicode(track["artist"], "utf-8"))

		if match_in_name or match_in_artist or match_in_name_kana or match_in_artist_kana:
			handler.add_new_item(title=track["name"], subtitle=track["artist"], arg=track["name"], icon=get_artwork(track["name"]))
			anything_matched = True

except:
	pass

if not anything_matched:
	if playlist_name == "":
		# get playlists
		sprocess = subprocess.Popen(["osascript", "get_playlists.scpt"], stdout=subprocess.PIPE)

		raw_playlists = sprocess.stdout.read()

		# remove empty line
		raw_playlists = raw_playlists[:-1]

		playlists = raw_playlists.split('\n')

		playlist_list = []

		if len(playlists) > 0:
			for playlist in playlists:
				stuff = playlist.split('!MAESTRO!')

				playlist_name = stuff[0]
				playlist_count = int(stuff[1])

				# don't show empty playlists
				if playlist_count > 0:
					playlist_list.append({"name": playlist_name, "count": playlist_count})

			for playlist in playlist_list:
				if handler.query.lower() in playlist["name"].lower():
					handler.add_new_item(title=playlist["name"], subtitle="%s songs in this playlist." % playlist["count"], icon="default.png", arg=playlist["name"])
		else:
			handler.add_new_item(title="No playlists found", icon="default.png")
	else:
		handler.add_new_item(title="Couldn't find a song which match '%s'" % handler.query, icon="default.png")

disallow_recache()

handler.push()

