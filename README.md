# RMSaP 1.0
Ridiculous Media Search and Play

The objective of this CLI Tool is do a fast search of media files and just play instantly 
using only native python libraries in a unix-like environment. If you really
want play something you should consider install mpv.

This software read some ID3 Tags, and use whoosh to index, but, don't play anything
using libraries like pygst, because as you can see, that is not the objective of
the application at all.

To Install you can link or copy to your path.

# Usage
rmsap.py [command] [search patterns]

rmsap.py play [search patterns]                         - Search media and play.

rmsap.py search [search patterns]                       - Search media and print paths.

rmsap.py build-list [FULL_PATH_OF_YOUR_MEDIA_FOLDER]    - Build your media list.


You can concatenate how many search patterns you need, using just spaces
between them.

# Examples

rmsap.py build-list /home/user/Music

rmsap.py search vivaldi spring

rmsap.py play chopin nocturne 2 d

rmsap.py play mozart 40

rmsap.py play bach
