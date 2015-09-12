#!/usr/bin/python
# -*- coding: utf-8 -*-
from sys import argv
from os import getenv
import gzip

media_types = ['.asx', '.dts', '.gxf', '.m2v', '.m3u', '.m4v', '.mpeg1', '.mpeg2', '.mts', '.mxf',
               '.ogm', '.pls', '.bup', '.a52', '.aac', '.b4s', '.cue', '.divx', '.dv', '.flv',
               '.m1v', '.m2ts', '.m4p', '.mkv', '.mov', '.mpeg4', '.oma', '.spx', '.ts', '.vlc',
               '.vob', '.xspf', '.dat', '.bin', '.ifo', '.part', '.3g2', '.avi', '.mpeg', '.mpg',
               '.flac', '.m4a', '.mp1', '.ogg', '.wav', '.xm', '.3gp', '.srt', '.wmv', '.ac3',
               '.asf', '.mod', '.mp2', '.mp3', '.mp4', '.wma', '.mka']

media_path = getenv("HOME")+'/.rmsp_media_path.gz'
playlist_path = '/tmp/playlist_rmsp'

if argv[1] == 'build-list':
    import subprocess
    import os.path
    proc = subprocess.Popen(['find', argv[2]], stdout=subprocess.PIPE)
    lista = gzip.open(media_path, 'wb')

    while True:
        line = proc.stdout.readline()
        if line != '':
            line = line.rstrip()
            if os.path.splitext(line)[1] in media_types:
                lista.write(line+'\n')
        else:
            lista.close()
            break

if argv[1] == 'play':
    from subprocess import call
    words = []

    for i in argv[2:]:
        words.append(i.lower())

    with gzip.open(media_path) as f:
        path_list = f.readlines()

    playlist = open(playlist_path, 'w')
    for path in path_list:
        print path
        count = 0
        for word in words:
            if word in path.lower():
                count = count + 1
        if count == len(words):
            playlist.write(path+'\n')
    playlist.close()
    call(['mplayer', '-playlist', playlist_path])
