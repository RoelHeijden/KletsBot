

import torch.nn as nn


class NeuralNet(nn.Module):
    """
    Neural network using the Torch module.

    Feed forward neural network:
        1 input layer with size == len(all unique words)
        1 output layer with size == len(all unique tags)
        1 hidden layer with ReLU activation
    """

    def __init__(self, input_size, output_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, output_size)
        self.activation = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.activation(out)
        out = self.l2(out)
        return out

