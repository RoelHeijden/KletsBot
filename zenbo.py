import os
import json
import re
import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace


class Zenbo:

    def __init__(self, show_emotion):
        #initial settings for text to speech and speech to text
        self.zenbo_speakSpeed = 100
        self.zenbo_speakPitch = 100
        self.zenbo_speakLanguage = 2
        self.zenbo_listenLanguageId = 1
        
        #connect to Zenbo
        self.zenbo = pyzenbo.connect('')
        
        
        self.show_emotion = show_emotion
        self.myUtterance = ''
        self.zenbo.robot.set_expression(RobotFace.DEFAULT)
        time.sleep(int(0.5))
        self.zenbo.robot.register_listen_callback(1207, self.listen_callback)
        time.sleep(int(1))

    def stop(self):
        self.zenbo.robot.unregister_listen_callback()
        self.zenbo.robot.set_expression(RobotFace.DEFAULT)
        self.zenbo.release()
        time.sleep(1)
        os._exit(0)

    def listen_callback(self, args):
        event_slu_query = args.get('event_slu_query', None)
        if event_slu_query and event_slu_query.get('app_semantic').get('correctedSentence') and event_slu_query.get('app_semantic').get('correctedSentence') != 'no_BOS':
            self.myUtterance = str(event_slu_query.get('app_semantic').get('correctedSentence'))
        if event_slu_query and event_slu_query.get('error_code') == 'csr_failed':
            self.myUtterance = ''
            
    def speak(self, message, emotion = RobotFace.PREVIOUS):
        if not self.show_emotion:
            emotion = RobotFace.DEFAULT
        self.robot.set_expression(emotion, message, {'speed':self.zenbo_speakSpeed, 'pitch':self.zenbo_speakPitch, 'languageId':self.zenbo_speakLanguage} , sync = True)

    def listen(self):
        self.robot.speak_and_listen('',{'listenLanguageId': self.zenbo_listenLanguageId})
        self.time.sleep(int(1))
        self.robot.stop_speak_and_listen()
        return self.myUtterance
