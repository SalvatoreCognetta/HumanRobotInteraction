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
    # im.setProfile(['*', '*', '*', '*']) # Setting universal language
    im.logenable() # Activating log to store the answers
    im.init()

    im.ask('welcome')
    im.ask('questionnaire')

    a = im.ask('l1')
    im.logdata('A1: '+a)
    a = im.ask('l2')
    im.logdata('A2: '+a)
    a = im.ask('l3')
    im.logdata('A3: '+a)
    a = im.ask('l4')
    im.logdata('A4: '+a)
    a = im.ask('l5')
    im.logdata('A5: '+a)
    
    a = im.ask('i1')
    im.logdata('A6: '+a)
    a = im.ask('i2')
    im.logdata('A7: '+a)
    a = im.ask('i3')
    im.logdata('A8: '+a)
    a = im.ask('i4')
    im.logdata('A9: '+a)
    a = im.ask('i5')
    im.logdata('A10: '+a)
    
    im.execute('goodbye')
    im.init()
    im.logclose()


if __name__ == "__main__":

    mws = ModimWSClient()

    # local execution
    mws.setDemoPathAuto(__file__)
    # remote execution
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')

    mws.run_interaction(task)
