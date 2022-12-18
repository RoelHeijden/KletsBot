"""
Class for experimenting with optimizing the way the network is trained.

Call experiment with the desired values to test multiple models one after the other while only varying one parameter.

- Not everything can be adjusted here, some changes require adjustments in training.py.
- A higher training accuracy or lower loss doesn't always mean the network is better, use common sense and experiment yourself.

"""

from nn_pipeline.training.training import Training
from nn_pipeline.data_processing.wordData import WordData
from nn_pipeline.data_processing.nlp import NLP


def experiment(network_params, independent_variable, output_settings, criterion, hidden_size=8, n_epochs=300, learning_rate=0.001,
               batch_size=10, train_size=0.75, val_size=0.25, use_val=True, use_acc=True, show_plots=True, save=False,
               train_file="data\\trainingdata.csv", save_location="data\\test_networks\\network"):
    """
    Function for comparing multiple models by varying one parameter at a time for each model.

    Possible independent variables:
    ["hidden_size", "n_epochs", "learning_rate", "batch_size", "train_size", "val_size"]


    :param network_params: List
        List of values, a new network is trained with the
        independent_variable equal to this value for each in the list

    :param: independent_variable: String
        The variable to be adjusted

    :param: output_settings: List
        Output class settings matching the models

    :param criterion: Pytorch opt
        Optimization function

    :param hidden_size: Int
        Hidden size of network

    :param n_epochs: Int
        Number of epochs to train

    :param learning_rate: Float
        How quickly the networks learn

    :param batch_size: Int
        Batch size for training networks

    :param train_size: Float
        Proportion of data that is used for training

    :param val_size: Float
        Proportion of data used for validation

    :param use_val: Boolean
        Use validation set True/False

    :param use_acc: Boolean
        Use accuracy test True/False

    :param show_plots:  Boolean
        Show plots of model training progressions True/False

    :param save: Boolean
        Save trained models to file True/False

    :param train_file: String
        File to train models from

    :param save_location: String
        Folder to store the networks
    """

    nlp = NLP()

    # reads the csv, init all_words and tags
    word_data = WordData(train_file, nlp)
    word_data.details()

    models = []
    for i, param in enumerate(network_params):
        save_file = save_location +str(i)+".pth"
        switcher = {
            # train criterion
            "criterion": Training(output_settings, param, hidden_size, n_epochs, learning_rate, batch_size, train_size, val_size, save_file, use_val, use_acc, False, save, train_file),
            # hidden_size=param
            "hidden_size": Training(output_settings, criterion, param, n_epochs, learning_rate, batch_size, train_size, val_size, save_file, use_val, use_acc, False, save, train_file),
            # n_epochs=param
            "n_epochs": Training(output_settings, criterion, hidden_size, param, learning_rate, batch_size, train_size, val_size, save_file, use_val, use_acc, False, save, train_file),
            # learning_rate=param
            "learning_rate": Training(output_settings, criterion, hidden_size, n_epochs, param, batch_size, train_size, val_size, save_file, use_val, use_acc, False, save, train_file),
            # batch_size=param
            "batch_size": Training(output_settings, criterion, hidden_size, n_epochs, learning_rate, param, train_size, val_size, save_file, use_val, use_acc, False, save, train_file),
            # train_size=param
            "train_size": Training(output_settings, criterion, hidden_size, n_epochs, learning_rate, batch_size, param, val_size, save_file, use_val, use_acc, False, save, train_file),
            # val_size=param
            "val_size": Training(output_settings, criterion, hidden_size, n_epochs, learning_rate, batch_size, train_size, param, save_file, use_val, use_acc, False, save, train_file)
        }
        model = switcher.get(independent_variable)
        model.train(word_data)
        models.append(model)

    if show_plots:
        # print loss and acc
        show(models, network_params, independent_variable)
        # plot loss and acc
        plot_loss_acc(models, network_params, independent_variable)

def plot_loss_acc(models, params, variable):
    """
    Plot graphs the progression of loss and accuracy of each model each model.

    :param models: List
        List of neural network models
    :param params: List
        Parameter values that where filled in for each models' dependent variable
    :variable: String
        Name of the dependent variable being tested
    :return: None
    """

    for i,m in enumerate(models):
        m.plot_loss_acc("Network {} {}={} loss and accuracy progression".format(i, variable, params[i]))


def show(models, params, variable):
    """
    Display the learning progression of each model.

    :param models: List
        Neural network models
    :param params: List
        Parameter values that where filled in for each models' dependent variable
    :variable: String
        Name of the dependent variable being tested
    :return: None
    """

    print("Models tested with variable {}".format(variable))
    for i, m in enumerate(models):
        print("model {}, parameter {}".format(i, params[i]))
        print("\ttrain_loss: ",m.train_loss[-1])
        print("\tval_loss: ", m.val_loss[-1])
        print("\ttrain_acc: ", m.train_acc[-1])
        print("\tval_loss: ",m.val_acc[-1])

