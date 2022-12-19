
class Labels:
    YES = 'yes'
    NO = 'no'
    # extend with more labels that would result in follow up questions if necessary


class Types:
    YES_NO = 'yes/no'
    OPEN_END = 'open ended'


class Topics:
    TOPIC = 'TOPIC'
    SPORTS = 'sport'
    MUSIC = 'music'
    # extend


class Question:
    def __init__(self, question, type, topic, follow_ups=None):
        self.question = question
        self.type = type
        self.topic = topic
        self.follow_ups = follow_ups

    def show(self):
        print(self.question)
        print(f'topic: \033[34m{self.topic}\033[0m')
        print(f'type: \033[34m{self.type}\033[0m')
        for label, follow_up in self.follow_ups.items():
            print(f'\033[34m{label}:\033[0m {follow_up}')


class Messages:
    def __init__(self):
        # responses
        self.please_reformulate = "I'm not sure what you mean. Could you reformulate your answer?"
        self.main_unknown = "Sorry I still don't understand. We'll skip this question."
        self.follow_up_unknown = "Sorry I'm not familiar with that " + Topics.TOPIC + ". Let's move on!"

        # main questions
        self.main_questions = [
            Question(
                question="Do you like sports?",
                type=Types.YES_NO,
                topic=Topics.SPORTS,
                follow_ups={
                    Labels.YES: Question("Which sport do you like most?", Types.OPEN_END, Topics.SPORTS)
                }
            ),
            Question(
                question="Do you like listening to music?",
                type=Types.YES_NO,
                topic=Topics.MUSIC,
                follow_ups={
                    Labels.YES: Question("What type of music do you like most?", Types.OPEN_END, Topics.MUSIC),
                    Labels.NO: Question("So you would also not enjoy live music, like a at concert?", Types.YES_NO, Topics.MUSIC)
                }
            ),
            # extend
        ]

    def list_all_questions(self):
        main_questions = [q.question for q in self.main_questions]
        follow_ups = [f.question for q in self.main_questions for f in list(q.follow_ups.values())]
        return main_questions + follow_ups

    def show_questions(self):
        for question in self.main_questions:
            print(''.join([char*40 for char in '-']))
            question.show()
            print()

    def send(self, message):
        print("Henk:", '\033[34m' + message + '\033[0m')

