#!/usr/bin/env python
"""from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "/home/frias/Documents/Innovacion/pocketsphinx/pocketsphinx-python/pocketsphinx/model"
DATADIR = "/home/frias/Documents/Innovacion/pocketsphinx/pocketsphinx-python/pocketsphinx/test/data"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
decoder = Decoder(config)

# Decode streaming data.
decoder = Decoder(config)
decoder.start_utt()
stream = open(path.join(DATADIR, 'goforward.raw'), 'rb')
while True:
  buf = stream.read(1024)
  if buf:
    decoder.process_raw(buf, False, False)
  else:
    break
decoder.end_utt()
print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])"""

"""
from pocketsphinx import LiveSpeech

speech = LiveSpeech(lm=False, keyphrase='forward', kws_threshold=1e+20)
for phrase in speech:
    print(phrase.segments(detailed=True))

"""


import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'es'),
    lm=os.path.join(model_path, 'es-20k.lm'),
    dic=os.path.join(model_path, 'es.dict')
)

for phrase in speech:
    if str(phrase) == 'hola':
        print('Gotcha')
        print(phrase.segments(detailed=True))
    #print(phrase)