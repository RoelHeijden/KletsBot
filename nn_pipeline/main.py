
import torch.nn as nn

from training.training import Training
from testing.testing import Testing
from training.trainingOptimizer import experiment


class Main:
    """
    Main class.

    Running this file allows you to:
        1) train the network
        2) train multiple networks (via trainOptimizer)
        3) test via chat
        4) quick test via test_questions.txt
        5) quick test multiple nn models
    """

    def __init__(self):
        """
        -- TrainingOptimizer parameters --
        network_params:       dependent variable values
        independent_variable: independent variable name

        -- File parameters --
        data_location:   Path to the data folder
        train_data_file: training data file path
        save_file:       save file path
        save_model:      save the trained model (True/False)

        -- Training parameters --
        hidden_size:   hidden size of network
        n_epochs:      n training iterations
        learning_rate: train learning rate
        batch_size:    train batches size
        criterion:     optimization function
        train_size:    train set size (1.00 >= train_size > 0.00)
        val_size:      test set size (1.00 > val_size >= 0.00)
        use_val:       use validation set (True/False)
        use_acc:       use accuracy test (True/False)
        show_plots:    show plots of model training progressions(True/False)

        -- NLP parameters --
        spellcheck_distance: maximum min-edit distance for words to be corrected
        n_gram_size:         size of the ngram tuples
        check_synonyms:      check for synonyms (True/False)

        -- Output parameters --
        model_file:               path to trained nn model
        filtered_tags:            tags to not be considered in the guess response
        respond_threshold:        bot answers if < probability
        guess_threshold:          bot gives estimated guesses if < probability
        guess_gap_perc_threshold: determines how quickly it groups multiple tags together for the guess response,
                                  multiple guesses if (prob[i] - prob[i+1])/prob[i+1] < guess_gap_perc_threshold
        max_guesses:              max amount of guesses grouped together
        """

        # self.train_data_file = "data\\trainingdata_yes_no.csv"
        # self.save_file = "data\\nn_yes_no.pth"
        # self.respond_threshold = 0.70
        # self.n_epochs = 10
        self.train_data_file = "data\\trainingdata_open_end.csv"
        self.save_file = "data\\nn_open_end.pth"
        self.respond_threshold = 0.55
        self.n_epochs = 20

        ################################################################################

        # trainingOptimizer parameters
        self.network_params = [10, 12, 14, 16]
        self.independent_variable = "n_epochs"

        # training parameters
        self.hidden_size = 65
        self.learning_rate = 0.01
        self.batch_size = 40
        self.criterion = nn.CrossEntropyLoss()
        self.train_size = 1.00
        self.val_size = 0.00
        self.use_val = False
        self.use_acc = False
        self.show_plots = False

        # output parameters
        self.use_guess_response = False
        self.model_file = self.save_file
        self.filtered_tags = ['Greeting', 'Ending']
        self.guess_threshold = 0.35
        self.guess_gap_perc_threshold = 0.60
        self.max_guesses = 3

        # random
        self.save_model = True

    def run(self):
        """
        Runs the main console.

        Allows you to run one or more sections of the program
            1) train the network
            2) train multiple networks (via trainOptimizer)
            3) test via chat
            4) quick test via test_questions.txt
            5) quick test multiple models

        It is possible to 'chain' multiple commands. For example:
        "143" will train, quick_test and then chat.

        :return: None
        """

        print("What do you want to do?")
        print("1) \033[34mtrain\033[0m")
        print("2) \033[34mtrainOptimizer\033[0m")
        print("3) \033[34mtest chat\033[0m")
        print("4) \033[34mquick test\033[0m")
        print("5) \033[34mquick test multiple models\033[0m")
        order = input("enter number(s): ")
        print()

        output_settings = [self.respond_threshold, self.guess_threshold, self.guess_gap_perc_threshold,
                           self.max_guesses, self.filtered_tags, self.use_guess_response]
        for n in order:
            if n == "1":
                t = Training(output_settings, self.criterion, self.hidden_size, self.n_epochs,
                             self.learning_rate, self.batch_size, self.train_size, self.val_size, self.save_file,
                             self.use_val, self.use_acc, self.show_plots, self.save_model, self.train_data_file)
                t.train()

            if n == "2":
                experiment(self.network_params, self.independent_variable, output_settings,
                           self.criterion, self.hidden_size, self.n_epochs, self.learning_rate, self.batch_size, self.train_size,
                           self.val_size, self.use_val, self.use_acc, self.show_plots, self.save_model, self.train_data_file)

            if n == "3":
                t = Testing(self.model_file)
                t.chat()

            if n == "4":
                t = Testing(self.model_file)
                t.quick_test()

            if n == "5":
                test_networks = ["data\\test_networks\\network" + str(i) + ".pth" for i in range(len(self.network_params))]
                for model in test_networks:
                    t = Testing(model)
                    t.quick_test()


if __name__ == '__main__':
    main = Main()
    main.run()

