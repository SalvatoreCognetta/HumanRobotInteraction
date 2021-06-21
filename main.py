import os, qi

pip = os.getenv('PEPPER_IP')
pport = 9559

if __name__ == "__main__":
	session = qi.Session()

	session.connect("tcp://{}:{}".format(pip, str(pport)))

	# ALDialog = session.service("ALDialog")
	# voice only
	tts_service = session.service("ALTextToSpeech")
	tts_service.setLanguage("English")
	tts_service.setParameter("speed", 90)
	tts_service.say("Hello world")
