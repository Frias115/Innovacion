#!/usr/bin/env python

import os
from pocketsphinx import LiveSpeech, get_model_path
from os import environ, path

#model_path = get_model_path()

MODELDIR = "pocketsphinx-python/pocketsphinx/model"
DATADIR = "pocketsphinx-pyton/pocketsphinx/test/data"

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(MODELDIR, 'es-es/es-es'),
    lm=os.path.join(MODELDIR, 'es-es/spanish.lm.bin'),
    dic=os.path.join(MODELDIR, 'es-es/spanish.dict')
)

print 'Escuchando...'
for phrase in speech:
    if str(phrase) == 'hola':
        print('Gotcha')
        print(phrase.segments(detailed=True))
    #print(phrase)

