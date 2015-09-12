#!/usr/bin/python
# -*- coding: utf-8 -*-
from sys import argv, exit
from os import getenv
import gzip

media_types = ['.asx', '.dts', '.gxf', '.m2v', '.m3u', '.m4v', '.mpeg1', '.mpeg2', '.mts', '.mxf',
               '.ogm', '.pls', '.bup', '.a52', '.aac', '.b4s', '.cue', '.divx', '.dv', '.flv',
               '.m1v', '.m2ts', '.m4p', '.mkv', '.mov', '.mpeg4', '.oma', '.spx', '.ts', '.vlc',
               '.vob', '.xspf', '.dat', '.bin', '.ifo', '.part', '.3g2', '.avi', '.mpeg', '.mpg',
               '.flac', '.m4a', '.mp1', '.ogg', '.wav', '.xm', '.3gp', '.srt', '.wmv', '.ac3',
               '.asf', '.mod', '.mp2', '.mp3', '.mp4', '.wma', '.mka']
media_path = getenv("HOME")+'/.rmsap_media_path.gz'
playlist_path = '/tmp/rmsap_playlist'


def search_media_path(words):
    try:
        with gzip.open(media_path) as f:
            path_list = f.readlines()
    except IOError:
        print('I cant found your list of paths, please build it.')
        print('You should execute: rmsap build-list FULL_PATH_OF_YOUR_MEDIA_FOLDER')
        exit()
    result = []
    for path in path_list:
        count = 0
        name, full_path = path.split(';;rmsap;;')
        for word in words:
            if word in name:
                count = count + 1
        if count == len(words):
            result.append(full_path)
    return result

if argv[1] == 'build-list':
    import subprocess
    import os.path
    proc = subprocess.Popen(['find', argv[2]], stdout=subprocess.PIPE)
    lista = gzip.open(media_path, 'wb')
    print('Building list, this can take long. Go look your WhatsApp.')
    while True:
        line = proc.stdout.readline()
        if line != '':
            line = line.rstrip()
            if os.path.splitext(line)[1] in media_types:
                name = line.strip(argv[2]).lower()
                lista.write(name+';;rmsap;;'+line+'\n')
        else:
            lista.close()
            break
    print('Done.')

if argv[1] == 'play':
    from subprocess import call
    words = []
    for i in argv[2:]:
        words.append(i.lower())
    playlist = open(playlist_path, 'w')
    lista = search_media_path(words)
    for path in lista:
            playlist.write(path)
    playlist.close()
    if len(lista) > 0:
        call(['mplayer', '-playlist', playlist_path])
    else:
        print('No matches found')

if argv[1] == 'search':
    words = []
    for i in argv[2:]:
        words.append(i.lower())
    lista = search_media_path(words)
    all_paths = ''
    for path in lista:
        print(path.strip('\n'))

if argv[1] == 'help':
    help_text = '''RMSaP 1.0
Usage: rmsap [command] [search patterns]

rmsap play [search patterns]                         - Search media and play.
rmsap search [search patterns]                       - Search media and print paths.
rmsap build-list [FULL_PATH_OF_YOUR_MEDIA_FOLDER]    - Build your media list.

You can concatenate how many search patterns you need, using just spaces between them.

Examples:
rmsap build-list /home/user/Music
rmsap search vivaldi spring
rmsap play chopin nocturne 2 d
rmsap play mozart 40
rmsap play bach
'''
    print(help_text)
