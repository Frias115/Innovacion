#!/usr/bin/env python

import os
import subprocess
from pocketsphinx import LiveSpeech
from os import environ, path
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("properties.txt", 'r') as stream:
    data_loaded = load(stream)

speech = LiveSpeech(**data_loaded)

words_to_ban = set(line.strip() for line in open('words_to_ban.txt'))

print 'Escuchando...'
for word in words_to_ban:
    print  word
for phrase in speech:
    for word in words_to_ban:
        if str(phrase) == word:
            print('Gotcha')
            subprocess.check_call(["gnome-screensaver-command", "-l"])
            print(phrase.segments(detailed=True))
            #print(phrase)

#email cada semana
#cambio de contraseña
#log y estadisticas