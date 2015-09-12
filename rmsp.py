#!/usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import call
from sys import argv

words = []
playlist_path = '/tmp/playlist_rmsp'
playlist = open(playlist_path, 'w')

for i in argv[1:]:
    words.append(i.lower())

with open('/Users/bruno/index_media.txt') as f:
    path_list = f.readlines()

for path in path_list:
    if words[0] in path:
        playlist.write(path+'\n')

playlist.close()

call(['mplayer', '-playlist', playlist_path])
