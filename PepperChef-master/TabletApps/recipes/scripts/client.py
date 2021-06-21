import sys
import time
import os
import random

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print "Please set MODIM_HOME environment variable to MODIM folder."
    sys.exit(1)

# Set MODIM_IP to connnect to remote MODIM server

import ws_client
from ws_client import *

def task():
    #im.setProfile(['*', '*', '*', '*']) # Setting universal language
    im.init()

    im.ask('welcome')
    a = im.ask('menu')

    if(a=='juice'):
        im.ask(a, timeout=60)
        im.ask('juice1', timeout=60)
        im.ask('juice2', timeout=60)
        im.execute('goodbye')
    elif(a=='carbonara'):
        im.ask(a, timeout=60)
        im.ask('carbonara1', timeout=60)
        im.ask('carbonara2', timeout=60)
        im.ask('carbonara3', timeout=60)
        im.execute('goodbye')
    elif(a=='crostata'):
        im.ask(a, timeout=60)
        im.ask('crostata1', timeout=60)
        im.ask('crostata2', timeout=60)
        im.ask('crostata3', timeout=60)
        im.execute('goodbye')

    im.init()


if __name__ == "__main__":

    mws = ModimWSClient()

    # local execution
    mws.setDemoPathAuto(__file__)
    # remote execution
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')

    mws.run_interaction(task)