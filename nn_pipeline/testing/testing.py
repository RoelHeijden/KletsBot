

from nn_pipeline.algorithm.output import Output
from nn_pipeline.data_processing.importExport import File
import pandas as pd


class Testing:
    """
    Main class for testing a trained neural network.
    """

    def __init__(self, filename):
        self.path = filename

    def chat(self):
        """
        Test the trained model via simulated chat in the console.

        'a' ends the chat.

        :return: None
        """

        file = File(self.path)
        output = Output(file)
        print("Starting chat - enter 'a' to quit")
        while True:

            topic = input("Insert topic\n")

            sentence = input("You: ")
            if sentence == 'a':
                print("aborted", end="\n\n")
                break

            print("Henk:", end=" ")
            answer, probs = output.respond(sentence, topic)
            print(answer[0])
            print('\033[34m' + probs + '\033[0m')

    def quick_test(self, test_file):
        """
        Runs the algorithm on multiple test questions contained in test_questions.csv and prints the accuracy.

        :return: None
        """

        print("Starting quick test")
        questions = pd.read_csv(test_file)
        file = File(self.path)
        output = Output(file)

        probs = []
        correct = 0
        for i in range(len(questions)):
            tag = questions['tag'][i]
            sentence = questions['sentence'][i]
            prob, pred = output.get_prob(sentence, tag)

            probs.append(prob.detach().numpy())
            if prob > output.respond_threshold:
                correct += 1

            print(f"{i + 1}. \033[34m{prob:.3f} {tag}\033[0m", end="")
            print(f"  predicted: {pred}")

        print(f"Correct: {correct}/{len(questions)}")
        avg = sum(probs)/len(questions)
        print(f"Average: {avg:.4f}")
        print()

