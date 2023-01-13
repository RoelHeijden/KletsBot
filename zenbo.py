import os
import json
import re
import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace, LanguageType
from messages import Expressions


class Zenbo:

    def __init__(self):
        # initial settings for text to speech and speech to text
        self.zenbo_speakSpeed = 100
        self.zenbo_speakPitch = 100
        self.zenbo_speakLanguage = 2
        self.zenbo_listenLanguageId = 2

        # connect to Zenbo
        host = '192.168.178.41'
        self.zenbo = pyzenbo.connect(host)

        self.myUtterance = ''
        self.zenbo.robot.set_expression(RobotFace.DEFAULT)

        time.sleep(int(0.5))

        self.zenbo.robot.register_listen_callback('E7AABB554ACB414C9AB9BF45E7FA8AD9', self.listen_callback)

        time.sleep(int(1))

        self.zenbo.utility.track_face(False, False)

    def stop(self):
        self.zenbo.robot.unregister_listen_callback()
        self.zenbo.robot.set_expression(RobotFace.DEFAULT)
        self.zenbo.release()
        time.sleep(1)
        os._exit(0)

    def listen_callback(self, args):
        event_slu_query = args.get('event_slu_query', None)
        if event_slu_query and event_slu_query.get('app_semantic').get('correctedSentence') and event_slu_query.get(
                'app_semantic').get('correctedSentence') != 'no_BOS':
            self.myUtterance = str(event_slu_query.get('app_semantic').get('correctedSentence'))
        if event_slu_query and event_slu_query.get('error_code') == 'csr_failed':
            self.myUtterance = ''

    def speak(self, message):
        self.zenbo.robot.set_expression('HAPPY', message,
                                        {'speed': self.zenbo_speakSpeed, 'pitch': self.zenbo_speakPitch,
                                         'languageId': self.zenbo_speakLanguage}, sync=True)

    def listen(self):
        self.zenbo.robot.wait_for_listen('', {'listenLanguageId': self.zenbo_listenLanguageId})
        print(self.myUtterance)
        return self.myUtterance

    def set_expression(self, expression):
        self.zenbo.robot.set_expression(self.get_robot_expression(expression), '',
                                        {'speed': self.zenbo_speakSpeed, 'pitch': self.zenbo_speakPitch,
                                         'languageId': self.zenbo_speakLanguage}, sync=True)

    def get_robot_expression(self, expression):
        switch = {
            Expressions.SAD: 'INNOCENT',
            Expressions.HAPPY: 'HAPPY',
            Expressions.UNCERTAIN: 'DOUBTING',
            Expressions.PLEASED: 'PLEASED ',
            Expressions.ACTIVE: 'ACTIVE',
            Expressions.WORRIED: 'WORRIED'

        }
        return switch.get(expression)