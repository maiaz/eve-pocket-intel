#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import subprocess
import time
import io
import os
import glob
import requests
import json


discord_bot = "https://discordapp.com/api/webhooks/000000/AAAAAA"
# replace <token> with your token
telegram_bot = "https://api.telegram.org/bot<token>/sendMessage"
# enter your chat ID [ https://api.telegram.org/bot<token>/getUpdates ]
telegram_chat = '000000000'

# input path to YOUR eve-client logs
intel_path = u'./Chatlogs/delve.imperium*.txt'


#system list to report  -> 'system-name': jumps to you
systems_dict = {'J-LPX7':0,'F-TE1T':1,'QY6-RK':1,'K-6K16':2,'D-3GIO':3,'W-KQPI':3,'319-3D':4,'PUIG-F':4,'GY6A-L':5,'YZ9-F6':5,'0HDC-8':5}




#-------------------------------------------------------------------------------------

#tunings for TTS discord
warning_word = { '0': 'ALERT', '1': 'WARNING', '2': '' , '3':'','4':'','5':''}


discord_payload = { "content": "", "username" : "intel", "tts" : "true" }
telegram_payload = { "chat_id": telegram_chat, "text" : ""}
headers = {'Content-Type': 'application/json'}



def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':



    print "start"

    # intel log file name
    latest = max(glob.iglob(intel_path), key=os.path.getctime)


    logfile =io.open( latest, mode="r", encoding='utf-16-le')

    loglines = follow(logfile)
    for line in loglines:
        print line,

        detect_system = [ k for k,v in systems_dict.items() if k in line ]

        #report only if system found in DICT
        if detect_system:

            jumps = systems_dict[detect_system[0]]



            intel_line = line[25:]

            intel_line = intel_line[intel_line.find(" > ")+3:]

            intel_line = ("%s [%d jumps] %s" % (warning_word[str(jumps)],jumps,intel_line))


            #send to telegram
            telegram_payload['text'] = intel_line
            result = requests.post(telegram_bot, data=json.dumps(telegram_payload), headers=headers)

            #send to discord
            discord_payload['content'] = intel_line.replace(" clr", " clear", 1)
            result = requests.post(discord_bot, data=json.dumps(discord_payload), headers=headers)

