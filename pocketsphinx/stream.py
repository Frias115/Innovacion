#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from pocketsphinx import LiveSpeech
import time
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def write_to_log(file, text):
    time_text = time.strftime('[%l:%M%p %z on %b %d, %Y ] ')
    file.write(time_text + text + '\n')
    file.flush()

if __name__ == '__main__':

    #We suppose properties.txt and email.txt have the required variables

    #Load properties
    try:
        with open("properties.txt", 'r') as stream:
            data_loaded = load(stream)
    except IOError, inst:
        print 'properties.txt not found: ', inst.errno, inst.strerror
        sys.exit()

    #Load email info
    try:
        with open("email.txt", 'r') as stream:
            email_info = load(stream)
    except IOError, inst:
        print 'email.txt not found: ', inst.errno, inst.strerror
        sys.exit()

    #Open log
    log = open('log.txt','w')

    #Initialize LiveSpeech
    speech = LiveSpeech(**data_loaded)

    #Load words that we are gonna ban
    try:
        open('words_to_ban.txt', 'r')
    except IOError, inst:
        print 'words_to_ban.txt not found: ', inst.errno, inst.strerror
        sys.exit()

    words_to_ban = set(line.strip() for line in open('words_to_ban.txt'))

    if len(words_to_ban) == 0:
        print 'words_to_ban.txt is empty'
        sys.exit()

    #Listening
    write_to_log(log, 'Program initialized.')
    print 'Listening...'
    for phrase in speech:
        #Checking if the words we are listening are in words_to_ban
        for word in words_to_ban:
            #Found a match, lock the computer
            if str(phrase) == word:
                write_to_log(log, 'Word banned: ' + word + ' Computer locked.')
                print('Gotcha')
                subprocess.check_call(["gnome-screensaver-command", "-l"])
                print(phrase.segments(detailed=True))

    write_to_log(log, 'Program terminated. ')

    #Append log.txt to history.txt
    log = open('log.txt', 'r')
    history = open('history.txt', 'a+')
    history.write(log.read())

    #Send a message with the log.txt attached via gmail
    msg = MIMEMultipart()
    msg['From'] = email_info.get('user')
    msg['To'] = COMMASPACE.join(email_info.get('to'))
    time_text = time.strftime('[%l:%M%p %z on %b %d, %Y ] ')
    msg['Subject'] = 'Log ' + time_text

    msg.attach(MIMEText(''))

    with open('log.txt', "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename('log.txt')
        )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename('log.txt')
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(email_info.get('user'), email_info.get('password'))
    server.sendmail(email_info.get('user'), email_info.get('to'), msg.as_string())
    server.quit()
