import argparse
import os
import qi
import sys

# Apps paths macros
rep_app = "TabletApps/recipes"
que_app = "TabletApps/questionnaire"
scripts = "scripts"

class cd:
    """
    Context manager for changing the
    current working directory
    """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def launchApp(app):
    """
    Launch the application provided as argument
    without changing the current directory
    """
    with cd(os.path.join(app, scripts)):
        os.system("python client.py")
    return

"""
Ingredient storage sector
"""

import re

def parseIngredientRequest(cargo):
    result = re.search('adding (.*) to your shopping', cargo)
    return result.group(1)

ingredient_lst = []
def storeIngredient(ingredient):
    ingredient_lst.append(ingredient)
    print 'current ingredient list: ' + str(ingredient_lst)
    return

teaching_flag = False

def cb_lastanswer(cargo):
    """
    Callback for handling Dialog/LastAnswer
    """
    global teaching_flag
    if "let's begin" in cargo:
        teaching_flag = True
        launchApp(rep_app)
    if "I hope your experience" in cargo:
        launchApp(que_app)
    if "I'm adding" in cargo:
        ingredient = parseIngredientRequest(cargo)
        print 'Ingredient to store: ' + ingredient
        storeIngredient(ingredient)
    return

last_cooking_step = ''


def cb_currentsentence(cargo):
    """
    Callback for handling ALTextToSpeech CurrentSentence event
    """
    global last_cooking_step
    global teaching_flag
    
    if teaching_flag is True and len(cargo) > 1 and 'repeat the last step' not in cargo:
        last_cooking_step = cargo
    # Going to handle repetitions
    if 'repeat the last step' in cargo:
        ALTextToSpeech.say(last_cooking_step)

    if 'want to leave an evaluation' in cargo:
        teaching_flag = False
    return

def main_app(session, topic_path):
    """
    Main routine for PepperChef.
    """
    # Get ALDialog service
    ALDialog = session.service('ALDialog')
    # Get ALMemory service
    ALMemory = session.service('ALMemory')

    # Setup ALDialog
    ALDialog.setLanguage('English')
    # Load the topic file provided via arguments
    topf_path = topic_path.decode('utf-8')
    topic_name = ALDialog.loadTopic(topf_path.encode('utf-8'))
    # Activate loaded topic
    ALDialog.activateTopic(topic_name)
    
    # Setup ALMemory
    lastAnswerSubscriber = ALMemory.subscriber('Dialog/LastAnswer')
    lastAnswerSubscriber.signal.connect(cb_lastanswer)
    currentWordSubscriber = ALMemory.subscriber('ALTextToSpeech/CurrentSentence')
    currentWordSubscriber.signal.connect(cb_currentsentence)

    # Setup ALSpeakingMovement
    ALSpeakingMovement = session.service('ALSpeakingMovement')
    ALSpeakingMovement.setEnabled(True)
    ALSpeakingMovement.setMode('contextual')    
    
    # Setup ALBackgroundMovement
    ALBackgroundMovement = session.service('ALBackgroundMovement')
    ALBackgroundMovement.setEnabled(True)

    # Setup ALTextToSpeech
    ALTextToSpeech = session.service('ALTextToSpeech')
    global ALTextToSpeech
    
    # Start the dialog engine
    ALDialog.subscribe('pepperchef_dialog')
    try:
        raw_input("\nSpeak to the robot using rules from the just loaded .top file. Press Enter when finished:")
    finally:
        # Stop the dialog engine
        ALDialog.unsubscribe('pepperchef_dialog')
        # Deactivate and unload the main topic
        ALDialog.deactivateTopic(topic_name)
        ALDialog.unloadTopic(topic_name)            
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot's IP address. If on a robot or a local Naoqi - use '127.0.0.1' (this is the default value).")
    parser.add_argument("--port", type=int, default=9559,
                        help="port number, the default value is OK in most cases")
    parser.add_argument("--topic-path", type=str, required=True,
                        help="absolute path of the dialog topic file (on the robot)")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://{}:{}".format(args.ip, args.port))
    except RuntimeError:
        print ("\nCan't connect to Naoqi at IP {} (port {}).\nPlease check your script's arguments."
               " Run with -h option for help.\n".format(args.ip, args.port))
        sys.exit(1)
    main_app(session, args.topic_path)
    
