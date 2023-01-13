
class Labels:
    YES = 'yes'
    NO = 'no'
    
    # extend with more labels that could result in follow up questions, if necessary


class Types:
    YES_NO = 'yes/no'
    OPEN_END = 'open ended'


class Topics:
    TOPIC = 'TOPIC'
    SPORTS = 'sport'
    MUSIC = 'music'
    # extend


class Expressions:
    NO_EXPRESSION = 'no expression'
    HAPPY = 'happy'
    SAD = 'sad'
    UNCERTAIN = 'uncertain'
    PLEASED = 'pleased '
    ACTIVE = 'active'
    WORRIED = 'worried'


class Question:
    def __init__(self, question, type, topic, expressions=None, follow_ups=None, reaction=None):
        self.question = question
        self.type = type
        self.topic = topic
        self.expressions = expressions
        self.follow_ups = follow_ups
        self.reaction = reaction

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
                expressions={
                    Labels.YES: Expressions.PLEASED,
                    Labels.NO: Expressions.SAD
                },
                follow_ups={
                    Labels.YES: Question("Which sport do you like most?", Types.OPEN_END, Topics.SPORTS)
                },
                reaction={
                    Labels.YES: 'Nice! I Like sports too, although I can not play them myself.',
                    Labels.NO: 'I agree, I do not like sports either, altough big reason is that I can not play any sport.'
                }
            ),
            Question(
                question="Do you like listening to music?",
                type=Types.YES_NO,
                topic=Topics.MUSIC,
                expressions={
                    Labels.YES: Expressions.HAPPY,
                    Labels.NO: Expressions.SAD
                },
                follow_ups={
                    Labels.YES: Question("What type of music do you like most?", Types.OPEN_END, Topics.MUSIC),
                    Labels.NO: Question("So you would also not enjoy live music, like a at concert?", Types.YES_NO, Topics.MUSIC,
                                        expressions={Labels.YES: Expressions.PLEASED, Labels.NO: Expressions.WORRIED},)
                }
            ),
            # extend
        ]

    def list_all_questions(self):
        all_questions = []

        for main_q in self.main_questions:
            all_questions.append(main_q.question)

            for follow_up_q in list(main_q.follow_ups.values()):
                all_questions.append(follow_up_q.question)

        return all_questions

    def show_questions(self):
        for question in self.main_questions:
            print(''.join([char*40 for char in '-']))
            question.show()
            print()

