
import random
from datetime import datetime
import time

from nn_pipeline.algorithm import output
from nn_pipeline.data_processing.importExport import File
from messages import Topics, Types, Messages, Question, Expressions
from zenbo import Zenbo


# Import DictWriter class from CSV module
from csv import DictWriter

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

        self.zenbo = Zenbo()

    def startConversation(self):
        #starts the conversation with the user by asking for their name
        self.zenbo.speak('Hey, nice to meet you. My name is Zenbo.')
        self.zenbo.speak('One thing you should know about me is that I can only hear what you tell me when my ears become blue.')
        self.zenbo.speak('Let me show you.')
        self.zenbo.speak('What is your name?')
        answer= self.zenbo.listen().split(' ')
        name = answer[len(answer)-1]
        self.zenbo.speak('Nice to meet you ' + name, Expressions.HAPPY)
        self.zenbo.speak('Is it okay if I ask you some questions?')
        self.zenbo.speak('That way we can get to know each other')
        
        reference_info = {'Name': name, 'Date and Time': datetime.now()}
        self.answer_labels = {**reference_info, **self.answer_labels}
        
        #classify answer of the user (yes/no)
        network = self.nn_yes_no
        answer = self.zenbo.listen()

        label = network.predicted_tags(answer, "")[0]

        #if label = Labels.YES:
        if label == 'yes':
            self.zenbo.speak('Perfect!')
            self.chat()
        else:
            self.zenbo.set_expression(Expressions.SAD)
            self.zenbo.speak('Okay, talk to you later then.')
            self.zenbo.stop()
        
    def chat(self):
        # chat loop
        while self.messages.main_questions:
            question = self.messages.main_questions.pop()
            self.ask_question(question)
        self.zenbo.speak("Those were all of my questions. I really enjoyed talking to you! See you later! Bye!", Expressions.HAPPY)

        self.store_answers('results.csv')
        self.zenbo.stop()

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

        label = network.predicted_tags(answer, question.topic)[0]
        
        # check if no matching label exists
        if not label:
            # ask question, get answer and find the label, again
            self.zenbo.set_expression(Expressions.UNCERTAIN)
            self.zenbo.speak(self.messages.please_reformulate)
            answer = self.zenbo.listen()

            label = network.predicted_tags(answer, question.topic)[0]

            # check if still no matching label exists
            if not label:
                label = answer
                # follow_up_questions should get a different "I don't know" response here
                if is_follow_up:
                    self.zenbo.speak(self.messages.follow_up_unknown, Expressions.SAD)
                else:
                    self.zenbo.speak(self.messages.main_unknown, Expressions.SAD)

        # store user's answer label
        self.answer_labels[question.question] = label
        
        expression = self.get_expression(question, label)
        if question.reactions is not None:
            # let Zenbo verbally react to the answer
            self.zenbo.speak(question.reactions.get(label), expression)
        else:
            self.zenbo.speak("That is good to know.", expression)

        # if the current question is a follow up question, end here
        if is_follow_up:
            return

        # get the corresponding follow_up_question - if it exists
        follow_up_question = question.follow_ups.get(label)

        if follow_up_question:
            # use the label network to check if the previous answer already contains the relevant label
            # e.g. prev answer was 'yes, I like football' -> label = football
            label = None
            if question.type == Types.YES_NO and follow_up_question.type == Types.OPEN_END:
                label = self.nn_open_end.predicted_tags(answer, question.topic)[0]

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
    
    # store answers in a CSV file
    def store_answers(self, filename):
        # Open CSV file in append mode
        # Create a file object for this file
        with open(filename, 'a') as f_object:
        
            # Pass the file object and a list
            # of column names to DictWriter()
            # You will get a object of DictWriter
            dictwriter_object = DictWriter(f_object, fieldnames=list(self.answer_labels.keys()))
        
            # Pass the dictionary as an argument to the Writerow()
            dictwriter_object.writerow(self.answer_labels)
        
            # Close the file object
            f_object.close()

if __name__ == "__main__":
    chatbot = KletsBot()
    chatbot.startConversation()
