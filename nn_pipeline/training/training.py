
import torch
from torch.utils.data import DataLoader
from nn_pipeline.data_processing.wordData import WordData
from nn_pipeline.data_processing.trainingData import TrainingData
from nn_pipeline.algorithm.neuralNetwork import NeuralNet
from nn_pipeline.data_processing.importExport import File
from nn_pipeline.data_processing.nlp import NLP
import numpy as np
import matplotlib.pyplot as plt


class Training:
    """
    Main class for traning the network.

    Adjust the parameters for different training results, these vary the properties of the neural network.
    """

    def __init__(self, output_settings, criterion, hidden_size=65, n_epochs=10, learning_rate=0.01, batch_size=40, train_size=0.75,
                 val_size=0.25, save_file="data.pth", use_val=True, use_acc=True, show_plots=True, save=True,
                 train_file="trainingdata.csv"):
        """
        :param output_settings: List
            Output class settings matching the models

        :param criterion: Pytorch opt
            Optimization function

        :param hidden_size: Int
            Hidden size of network

        :param n_epochs: Int
            Number of epochs to train

        :param learning_rate: Float
            How quick the networks learn

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

        :param model_file: String
            Name of file where the (trained) nn model will be exported

        :param train_file: String
            Name of file containing training data

        """
        self.output_settings = output_settings
        self.model_file = save_file
        self.train_file = train_file

        self.hidden_size = hidden_size
        self.n_epochs = n_epochs
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.criterion = criterion

        self.train_size = train_size
        self.val_size = val_size

        self.use_val = use_val
        self.use_acc = use_acc
        self.show_plots = show_plots
        self.save_state = save

        # for storing loss and acc
        self.avg_train_loss = None
        self.avg_val_loss = None
        self.avg_train_acc = None
        self.avg_val_acc = None

    def train(self, preloaded_words=None):
        """
        Inits the data, model and starts training of the network.

        :return: None
        """
        print("Starting training")
        print("Note: this may take a while")

        # init nlp with given settings
        nlp = NLP()

        if preloaded_words:
            word_data = preloaded_words
        else:
            # reads the csv, init all_words and tags
            word_data = WordData(self.train_file, nlp)
            word_data.details()

        # converts data to binary, init Dataset class for Torch
        training_data = TrainingData(word_data, nlp)

        # init neural network model
        input_size = len(word_data.all_words) + len(word_data.topics)
        output_size = training_data.n_tags
        model = NeuralNet(input_size, output_size, self.hidden_size)

        # define train, val, test splits
        train_size = round(self.train_size*len(training_data))
        val_size = round(self.val_size*len(training_data))

        train_data, val_data = torch.utils.data.random_split(training_data, [train_size, val_size])

        # training the model
        if self.use_val:
            self.train_loss, self.val_loss, self.train_acc, self.val_acc = self.train_network(model, train_data, val_data)
        else:
            self.train_loss, self.val_loss, self.train_acc, self.val_acc = self.train_network(model, training_data)

        # Plot loss and acc per epoch of model
        if self.show_plots:
            self.plot_loss_acc()

        # saving the model state
        if self.save_state:
            file = File(self.model_file)
            file.save(model, word_data, self.output_settings)

    def train_network(self, model, train_data, val_data=None, loss_info_interval=20):
        """
        Trains the model.

        :param train_data: DataSet()
            Training data of network
        :param val_data: DataSet()
            Validation data of network
        :param model: (untrained) neural network
            Initialized parameters of model

        :return: None
        """

        train_loader = DataLoader(dataset=train_data, batch_size=self.batch_size, shuffle=True)

        if val_data is not None:
            val_loader = DataLoader(dataset=val_data, batch_size=self.batch_size, shuffle=True)
        else:
            val_loader = train_loader

        optimizer = torch.optim.Adam(model.parameters(), lr=self.learning_rate, weight_decay=0.00001)

        # average losses and accuracy per epoch
        avg_train_loss = np.zeros(self.n_epochs)
        avg_val_loss = np.zeros(self.n_epochs)
        avg_train_acc = np.zeros(self.n_epochs)
        avg_val_acc = np.zeros(self.n_epochs)

        for epoch in range(self.n_epochs):

            # training
            for i, (words, labels) in enumerate(train_loader):

                words = words.to(dtype=torch.float)
                labels = labels.to(dtype=torch.long)

                # forward pass
                output = model(words)
                train_loss = self.criterion(output, labels)
                avg_train_loss[epoch] += train_loss.item() / len(train_data)

                # backwards pass
                optimizer.zero_grad()
                train_loss.backward()
                optimizer.step()

                # update the weights
                with torch.no_grad():
                    for p in model.parameters():
                        p -= self.learning_rate * p.grad

            if val_data != None:

                # validation
                for words, labels in val_loader:

                    words = words.to(dtype=torch.float)
                    labels = labels.to(dtype=torch.long)

                    # forward pass
                    output = model(words)
                    val_loss = self.criterion(output, labels)
                    avg_val_loss[epoch] += val_loss.item() / len(train_data)

                # Show loss
                if (epoch + 1) % loss_info_interval == 0:
                    print(f'Loss epoch {epoch + 1}/{self.n_epochs}: \n\ttrain loss={avg_train_loss[epoch]:.4f}, \t val loss={avg_val_loss[epoch]:.4f}')

            # train loss only
            else:
                if (epoch + 1) % loss_info_interval == 0:
                    print(f'Loss epoch {epoch + 1}/{self.n_epochs}: \n\ttrain loss={avg_train_loss[epoch]:.4f}')

            if self.use_acc:
                # Accuracy test on classifying training and validation data
                avg_train_acc[epoch], avg_val_acc[epoch] = self.accuracy_test(train_loader, val_loader, epoch, model, train_data, val_data, loss_info_interval)

        if self.use_val:
            print(f'training complete, final average train loss={avg_train_loss[-1]:.4f}, final average val loss={avg_val_loss[-1]:.4f}')
        else:
            print(f'training complete, final average train loss={avg_train_loss[-1]:.4f}')

        if self.use_acc:
            print(f'final average train accuracy={avg_train_acc[-1]:.4f}, final average val accuracy={avg_val_acc[-1]:.4f}')

        return avg_train_loss, avg_val_loss, avg_train_acc, avg_val_acc


    def accuracy_test(self, train_loader, val_loader, epoch, model, train_data, val_data, loss_info_interval):
        """
        Model accuracy on training and validation data for 1 epoch.

        :param train_loader: DataLoader()
            Pytorch training loader
        :param val_loader: DataLoader()
            Pytorch validation loader
        :param epoch: Int
            Current epoch
        :param model: NeuralNetwork
            Model that is being tested
        :param train_data: DataSet()
            Training data
        :param val_data: DataSet()
            Validation data
        :param loss_info_interval: Int
            How many epochs should pass before printing accuracy to the console
        :return:
            train_accuracy: Float
            val_accuracy: Float
        """

        train_accuracy = 0
        val_accuracy = 0

        with torch.no_grad():
            # train accuracy
            for i, (words, labels) in enumerate(train_loader):

                words = words.to(dtype=torch.float)
                labels = labels.to(dtype=torch.long)

                output = model(words)
                _, pred_labels = torch.max(output.data, 1)

                train_accuracy += (pred_labels == labels).sum().item()
            train_accuracy = train_accuracy / len(train_data)

            if val_data != None:
                # validation accuracy
                for i, (words, labels) in enumerate(val_loader):
                    words = words.to(dtype=torch.float)
                    labels = labels.to(dtype=torch.long)

                    output = model(words)
                    _, pred_labels = torch.max(output.data, 1)

                    val_accuracy += (pred_labels == labels).sum().item()
                val_accuracy = val_accuracy / len(val_data)

                # show accuracy
                if (epoch + 1) % loss_info_interval == 0:
                    print(f'Accuracy epoch {epoch + 1}/{self.n_epochs}: \n\ttrain acc={train_accuracy:.4f}, \t val acc={val_accuracy:.4f}')

            else:
                # train accuracy only
                if (epoch + 1) % loss_info_interval == 0:
                    print(f'Accuracy epoch {epoch + 1}/{self.n_epochs}: \n\ttrain acc={train_accuracy:.4f}')

        return train_accuracy, val_accuracy

    def plot_loss_acc(self, fig_title="loss and accuracy progression of neural network"):
        """
        Plot loss and accuracy training progression for the model.

        :param fig_title: String
            Title of figure
        :return: None
        """

        fig, ax = plt.subplots(4, figsize=(20,20))
        fig.suptitle(fig_title)

        def plotter(data, title, y, x, nr):
            ax[nr].plot(data)
            ax[nr].set_title(title)
            ax[nr].set_ylabel(y)
            ax[nr].set_xlabel(x)
        plotter(self.train_loss, "Training loss", "training loss", "nr of training epochs", 0)
        plotter(self.val_loss, "Validation loss", "validation loss", "nr of training epochs", 1)
        plotter(self.train_acc, "Training accuracy", "training accuracy", "nr of training epochs", 2)
        plotter(self.val_acc, "Validation accuracy", "validation accuracy", "nr of training epochs", 3)
        plt.show()


