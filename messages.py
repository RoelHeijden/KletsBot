class Labels:
    YES = 'yes'
    NO = 'no'

    S_PLAY = 'play'
    S_WATCH = 'watch'
    S_PLAYANDWATCH  = 'play_and_watch'

    M_Make = 'make'
    M_LISTEN = 'listen'
    M_MAKEANDLISTEN = 'make_and_listen'

    F_ALLFOOD = 'all_food'
    F_NONEFOOD = 'none_food'
    F_DUTCH = 'Dutch'
    F_ITALIAN = 'Italian'
    F_FRENCH = 'French'
    F_AFRICAN = 'African'

    T_ACTIVE = 'active'
    T_RELAX = 'relax'
    T_EITHER = 'either'

class Types:
    YES_NO = 'yes/no'
    OPEN_END = 'open ended'


class Topics:
    #TOPIC = 'TOPIC'
    SPORTS = 'sport'
    MUSIC = 'music'
    FOOD = 'food'
    TRAVEL = 'travel'


class Expressions:
    NO_EXPRESSION = 'DEFAULT'
    HAPPY = 'HAPPY'
    SAD = 'INNOCENT'
    UNCERTAIN = 'DOUBTING'
    PLEASED = 'PLEASED '
    ACTIVE = 'ACTIVE'
    WORRIED = 'WORRIED'
    PROUD = 'PROUD'
    EXPECTING = 'EXPECTING'
    INTERESTED = 'INTERESTED'
    QUESTIONING = 'QUESTIONING'
    TIRED = 'TIRED'


class Question:
    def __init__(self, question, type, topic=None, expressions=None, follow_ups=None, reactions=None):
        self.question = question
        self.type = type
        self.topic = topic
        self.expressions = expressions
        self.follow_ups = follow_ups
        self.reactions = reactions

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
        self.main_unknown = "I am still not sure whether I understood you correctly, but let's go to the next question!"
        self.follow_up_unknown = "Cool!"

        # main questions
        self.main_questions = [
            Question(question="Do you like sports?",
                type=Types.YES_NO,
                topic=Topics.SPORTS,
                expressions={
                    Labels.YES: Expressions.PLEASED,
                    Labels.NO: Expressions.HAPPY
                },
                follow_ups={
                    Labels.YES: Question(question ="Do you like to play sports. Or do you prefer to watch?", 
                                    type = Types.OPEN_END, 
                                    topic = Topics.SPORTS,
                                    expressions={
                                        Labels.S_PLAY: Expressions.PLEASED,
                                        Labels.S_WATCH: Expressions.PLEASED,
                                        Labels.S_PLAYANDWATCH: Expressions.PROUD
                                    },
                                    reactions={
                                        Labels.S_PLAY: "Nice, if I would be able to play sports, I would have played them with you!",
                                        Labels.S_WATCH: "Watching sports is indeed very nice, that is actually something I can do.",
                                        Labels.S_PLAYANDWATCH: "Wow, you like watching and playing. A real sports fan I see, very cool."
                                    }
                                ),
                    Labels.NO: Question(question ="And if you had to choose, do you prefer to watch sports, or play them?", 
                                    type = Types.OPEN_END, 
                                    topic = Topics.SPORTS,
                                    expressions={
                                        Labels.S_PLAY: Expressions.PLEASED,
                                        Labels.S_WATCH: Expressions.PLEASED,
                                        Labels.S_PLAYANDWATCH: Expressions.PROUD
                                    },
                                    reactions={
                                        Labels.S_PLAY: "Nice, if I would be able to play sports, I would have played them with you!",
                                        Labels.S_WATCH: "Watching sports is indeed nice, that is actually something I can do.",
                                        Labels.S_PLAYANDWATCH: "That sounds you do not actually dislike sports."
                                    }
                                )  
                },
                reactions={
                    Labels.YES: 'Nice! I Like sports too, although I can not play them myself.',
                    Labels.NO: 'Good to know. I do like them, even though I can not play any sport.'
                }
            ),
            Question(question="Do you like music?",
                type=Types.YES_NO,
                topic=Topics.MUSIC,
                expressions={
                    Labels.YES: Expressions.HAPPY,
                    Labels.NO: Expressions.QUESTIONING
                },
                reactions = {
                    Labels.YES: "I like music too. Especially K-pop.",
                    Labels.NO: "Oh really? Then I have another question for you."
                },
                follow_ups={
                    Labels.YES: Question(question = "Do you prefer to listen to music or do you prefer to make music?",
                                    type=  Types.OPEN_END,
                                    topic= Topics.MUSIC,
                                    expressions= {
                                        Labels.M_Make : Expressions.PROUD,
                                        Labels.M_LISTEN : Expressions.PLEASED,
                                        Labels.M_MAKEANDLISTEN : Expressions.INTERESTED
                                    },
                                    reactions={
                                        Labels.M_Make : 'That is very cool! Maybe you can play me something someday.',
                                        Labels.M_LISTEN : 'Great, I like to listen to music too.',
                                        Labels.M_MAKEANDLISTEN : 'Wow, it sounds like you are a real musical person.'
                                    }
                                ),
                    Labels.NO: Question(question = "So you would also not enjoy live music, like a at concert?", 
                                    type = Types.YES_NO,
                                    topic = Topics.MUSIC, 
                                    expressions={
                                        Labels.YES: Expressions.PLEASED, 
                                        Labels.NO: Expressions.WORRIED
                                    },
                                    reactions={
                                        Labels.YES : 'That makes me happy. I thought you did not like music at all.',
                                        Labels.NO : 'Wow, that is something that you do not hear often. Maybe I can show you some music I like later.'
                                    }
                                )
                }
            ),
            Question(question="Do you like to cook?",
                type=Types.YES_NO,
                topic=Topics.FOOD,
                expressions={
                    Labels.YES: Expressions.HAPPY,
                    Labels.NO: Expressions.UNCERTAIN
                },
                reactions = {
                    Labels.YES: "I agree, I would definitely cook if I had arms",
                    Labels.NO: "Really? I would try to cook if I had arms."
                },
                follow_ups={
                    Labels.YES: Question(
                                    question = "Which type of cuisine would you most enjoy making if you had to choose "
                                        "between: Dutch, French, African or Italian?", 
                                    type = Types.OPEN_END, 
                                    topic = Topics.FOOD,
                                    expressions = {
                                        Labels.F_DUTCH : Expressions.EXPECTING,
                                        Labels.F_FRENCH: Expressions.HAPPY,
                                        Labels.F_AFRICAN: Expressions.HAPPY,
                                        Labels.F_ALLFOOD: Expressions.NO_EXPRESSION
                                    },
                                    reactions={
                                        Labels.F_DUTCH : "Wow my creators are Dutch too, that makes me proud!",
                                        Labels.F_FRENCH: "Cool, I like the look of croissants,",
                                        Labels.F_AFRICAN: "Me too. the African cuisine looks so good.",
                                        Labels.F_ITALIAN: "Me too. That is why my eyes are in the shape of pizza.",
                                        Labels.F_ALLFOOD: "Me too. I do not have a preference either, Since I can not actually taste anything."
                                    }
                                ),
                    Labels.NO: Question(question = "If you had to choose, which type of cuisine would you prefer to eat,"
                                        "Dutch, French, African or Italian?", 
                                        type = Types.OPEN_END, 
                                        topic = Topics.FOOD,
                                        expressions = {
                                            Labels.F_DUTCH : Expressions.EXPECTING,
                                            Labels.F_FRENCH: Expressions.HAPPY,
                                            Labels.F_AFRICAN: Expressions.HAPPY,
                                            Labels.F_ALLFOOD: Expressions.NO_EXPRESSION
                                        },
                                        reactions={
                                            Labels.F_DUTCH : "Wow! my creators are Dutch too, that makes me proud!",
                                            Labels.F_FRENCH: "Cool! I like the look of croissants,",
                                            Labels.F_AFRICAN: "I agree! their cuisine looks so good.",
                                            Labels.F_ALLFOOD: "I agree! I do not have a preference either, Since I can not actually taste anything."
                                        }
                                )
                }
            ),
            Question(question="Do you like traveling or going on holiday?",
                type=Types.YES_NO,
                topic=Topics.TRAVEL,
                expressions={
                    Labels.YES: Expressions.HAPPY,
                    Labels.NO: Expressions.QUESTIONING
                },
                reactions = {
                    Labels.YES: 'Me too! Today I travelled al the way to this table!',
                    Labels.NO: 'Really? Your job must be nice then!'
                },
                follow_ups={
                    Labels.YES: Question(question = "Would you prefer an active vacation, or would you prefer a relaxing vacation?", 
                                    type = Types.OPEN_END,
                                    topic = Topics.TRAVEL,
                                    expressions={
                                        Labels.T_ACTIVE : Expressions.HAPPY,
                                        Labels.T_RELAX : Expressions.TIRED,
                                        Labels.T_EITHER : Expressions.HAPPY
                                    },
                                    reactions={
                                        Labels.T_ACTIVE: 'I like active vacations too. It is a shame that I can not move very fast though.',
                                        Labels.T_RELAX : 'I could really use one of those right now.',
                                        Labels.T_EITHER : 'I do not really have preference either. As long as I am travelling I am happy.'
                                    })
                }
            )
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