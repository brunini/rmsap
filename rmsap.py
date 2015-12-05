#!/usr/bin/python
# -*- coding: utf-8 -*-
from sys import argv
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

media_types = ['.asx', '.dts', '.gxf', '.m2v', '.m3u', '.m4v', '.mpeg1', '.mpeg2', '.mts', '.mxf',
               '.ogm', '.pls', '.bup', '.a52', '.aac', '.b4s', '.cue', '.divx', '.dv', '.flv',
               '.m1v', '.m2ts', '.m4p', '.mkv', '.mov', '.mpeg4', '.oma', '.spx', '.ts', '.vlc',
               '.vob', '.xspf', '.dat', '.bin', '.ifo', '.part', '.3g2', '.avi', '.mpeg', '.mpg',
               '.flac', '.m4a', '.mp1', '.ogg', '.wav', '.xm', '.3gp', '.srt', '.wmv', '.ac3',
               '.asf', '.mod', '.mp2', '.mp3', '.mp4', '.wma', '.mka']
media_path = os.getenv("HOME")+'/.rmsap_media_path'
playlist_path = '/tmp/rmsap_playlist'
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)


def search_media_path(busca):
    words = u''
    for i in busca:
        words = words + ' ' + unicode(i)
    try:
        ix = open_dir(media_path)
    except OSError:
        print('I cant found your list of paths, please build it.')
        print('You should execute: rmsap build-list FULL_PATH_OF_YOUR_MEDIA_FOLDER')
    saida = []
    print words
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(words)
        results = searcher.search(query)
        for item in results:
            saida.append(item['path'])
    return saida

if argv[1] == 'build-list':
    import time
    t0 = time.time()
    import taglib
    print('Building list, this can take long. Go look your WhatsApp.')
    os.mkdir(media_path)
    ix = create_in(media_path, schema)
    writer = ix.writer()
    full_path = unicode(argv[2])
    files = []
    for fqdn in [os.path.join(dp, f) for dp, dn, fn in
                 os.walk(full_path) for f in fn]:
        name = unicode(fqdn.split('/')[-1:][0])
        if os.path.splitext(name)[1] in media_types:
            print fqdn
            try:
                f = taglib.File(fqdn)
                tags = f.tags
                tmp = tags['ALBUM'][0] + ' ' + tags['ARTIST'][0] + ' ' + tags['TITLE'][0]
            except:
                tmp = ''
            writer.add_document(title=name, path=fqdn, content=name + ' ' + tmp)
    writer.commit()
    t1 = time.time()
    m, s = divmod((t1 - t0), 60)
    h, m = divmod(m, 60)
    print('Done in %02d:%02d:%02d' % (h, m, s))

if argv[1] == 'play':
    from subprocess import call
    lista = search_media_path(argv[2:])
    playlist = open(playlist_path, 'w')
    for path in lista:
        playlist.write(path.encode('utf8')+'\n')
    playlist.close()
    if len(lista) > 0:
        call(['mpv', '-playlist', playlist_path])
    else:
        print('No matches found')

if argv[1] == 'search':
    lista = search_media_path(argv[2:])
    for path in lista:
        print(path)

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
