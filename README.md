# RMSaP 1.0
Ridiculous Media Search and Play

The objective of this CLI Tool is do a fast search of media files and just play instantly 
using only native python libraries in a unix-like environment. If you really
want play something you should consider install mplayer or cvlc.

This software don't read ID3 Tags, don't use any type of standard database, and don't play anything
using librarys like pygst, because as you can see, that is not the objective of
the application at all. 


# Usage
rmsap [command] [search patterns]

rmsap play [search patterns]                         - Search media and play.

rmsap search [search patterns]                       - Search media and print paths.

rmsap build-list [FULL_PATH_OF_YOUR_MEDIA_FOLDER]    - Build your media list.


You can concatenate how many search patterns you need, using just spaces
between them.

# Examples

rmsap build-list /home/user/Music

rmsap search vivaldi spring

rmsap play chopin nocturne 2 d

rmsap play mozart 40

rmsap play bach
