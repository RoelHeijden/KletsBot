
from nn_pipeline.algorithm import output
from nn_pipeline.data_processing.importExport import File
from messages import Topics, Types, Messages, Question, Expressions

import random


class KletsBot:
    def __init__(self):
        # init the message class with the main questions in a random order
        self.messages = Messages()
        random.shuffle(self.messages.main_questions)

        # yes/no network
        model_file1 = "nn_pipeline\\data\\nn_yes_no.pth"
        self.nn_yes_no = output.Output(File(model_file1))

        # open end network
        model_file2 = "nn_pipeline\\data\\nn_open_end.pth"
        self.nn_open_end = output.Output(File(model_file2))

        # the final answers, formatted as {question: label} -- note: each label is initialized as '-'
        self.answer_labels = {str(question): '-' for question in self.messages.list_all_questions()}

    def chat(self):
        # chat loop
        if self.messages.main_questions:
            question = self.messages.main_questions.pop()
            self.ask_question(question)

        # show result
        print("\n---- final answers ----")
        for item in self.answer_labels.items():
            print(f'{item[0]} \033[34m{item[1]}\033[0m')

    def ask_question(self, question: Question, is_follow_up=False):
        # select the correct network based on question type
        network = None
        if question.type == Types.YES_NO:
            network = self.nn_yes_no
        elif question.type == Types.OPEN_END:
            network = self.nn_open_end

        # ask question, get answer and find the label
        self.zenbo.speak(question.question)
        answer = self.zenbo.listen()
        label = network.predicted_tags(answer)[0]
        self.zenbo.set_expression(self.get_expression(question, label))

        # check if no matching label exists
        if not label:
            # ask question, get answer and find the label, again
            self.zenbo.set_expression(Expressions.UNCERTAIN)
            self.zenbo.speak(self.messages.please_reformulate)
            answer = self.zenbo.listen()

            label = network.predicted_tags(answer)[0]

            # check if still no matching label exists
            if not label:
                self.zenbo.set_expression(Expressions.SAD)
                # follow_up_questions should get a different "I don't know" response here
                if is_follow_up:
                    self.zenbo.speak(self.messages.follow_up_unknown.replace(Topics.TOPIC, question.topic))
                else:
                    self.zenbo.speak(self.messages.main_unknown)

                # no label was found for the question -> return
                return

        # store user's answer label
        self.answer_labels[question.question] = label

        # if the current question is a follow up question, end here
        if is_follow_up:
            return

        try:
            # let Zenbo verbally react to the answer
            reaction = question.reaction.get(label)
            self.zenbo.speak(reaction)
        except:
            self.zenbo.speak('Good to know!')

        # get the corresponding follow_up_question - if it exists
        follow_up_question = question.follow_ups.get(label)

        if follow_up_question:
            # use the label network to check if the previous answer already contains the relevant label
            # e.g. prev answer was 'yes, I like football' -> label = football
            label = None
            if question.type == Types.YES_NO and follow_up_question.type == Types.OPEN_END:
                label = self.nn_open_end.predicted_tags(answer)[0]

            # if the answer already contained a label -> no need to ask the follow up question
            if label:
                self.answer_labels[follow_up_question.question] = label
            else:
                self.ask_question(follow_up_question, is_follow_up=True)

    def get_expression(self, question, label):
        if question.expressions:
            expression = question.expressions.get(label)
        else:
            expression = Expressions.NO_EXPRESSION
        return expression


if __name__ == "__main__":
    chatbot = KletsBot()
    chatbot.chat()
