
import torch
import numpy as np
from nn_pipeline.data_processing.nlp import NLP


class Output:
    """
    Class for getting the correct output response.

    Finds the correct response by:
    - Activating the NN
    - Matching the tags based on the output probabilities
    """

    def __init__(self, file):
        """
        :param file: .pth file
            File containing the NN model, data and class settings:

                model: Torch model state
                    Trained NN weights

                raw_data: Dictionary
                    All training patterns, tags and responses

                all_words: List
                    All unique words from the training data

                tags: List
                    All unique tags

                output_settings: List
                    Output class settings matching the model
        """

        self.model, self.raw_data, self.all_words, self.tags, output_settings = file.load()

        self.respond_threshold = output_settings[0]
        self.guess_threshold = output_settings[1]
        self.gap_ratio_threshold = output_settings[2]
        self.max_guesses = output_settings[3]
        self.filtered_tags = output_settings[4]
        self.use_guess_response = output_settings[5]

        self.nlp = NLP()
        self.model.eval()

    def to_input_array(self, sentence):
        """
        Creates a binary word occurrence array.

        :param sentence: String
            Multiple words in a logical sequence
        :return: [[float]] {0, 1} of length len(all_words)
        """

        # remove punctuation, check spelling, tokenize and lemmatize
        sentence = self.nlp.remove_punctuation(sentence)
        sentence = self.nlp.check_spelling(sentence)
        tokens = self.nlp.tokenize(sentence)
        tokens = self.nlp.lemmatize(tokens)

        x = np.zeros(len(self.all_words))

        for input_word in tokens:

            # get synonyms?

            for i, word in enumerate(self.all_words):

                # check synonyms?

                if input_word == word:
                    x[i] = 1

        x = x.reshape(1, x.shape[0])
        x = torch.from_numpy(x)
        x = x.to(dtype=torch.float)
        return x

    def respond(self, sentence):
        """
        Finds the correct response matching the tags.

        :param sentence: String
            Multiple words in a logical sequence
        :param pred_tags: None, tag or list of tags
            Predicted tags
        :return:
            answer: String
            tags: None/String/List
            responses: None/String/List
            probs: String
        """

        # Gets the predicted tags and probabilities
        pred_tags, probs = self.predicted_tags(sentence)

        # None response
        if pred_tags is None:
            return ("Sorry, I don't understand.", None), probs

        # Guess response
        elif isinstance(pred_tags, list):
            tags = [tag for tag in pred_tags if tag not in self.filtered_tags]

            if len(tags) == 0:
                return ("Sorry, I don't understand.", None), probs

            answer = "I'm not sure what you mean. Are you asking about:"
            for tag in tags:
                answer += '\n' + tag

            return (answer, tags), probs

        # normal response
        else:
            tag = pred_tags
            for section in self.raw_data:
                if section['tag'] == tag:
                    return ('insert answer for <' + tag + '>', tag), probs

    def predicted_tags(self, sentence):
        """
        Uses the output of the model to get all possible tags.

        :param sentence: String
            Multiple words in a logical sequence
        :return:
            tag, a list of tags, or None
            probs_string: String
        """

        x = self.to_input_array(sentence)
        nn_output = self.model(x)
        probs = torch.softmax(nn_output, dim=1)[0]
        _, pred = torch.max(nn_output, dim=1)

        ps, indices = probs.sort(descending=True)
        probs_string = ""
        for p, idx in zip(ps, indices):
            probs_string = probs_string + f'{p:.3f}: {self.tags[idx]}\n'

        if probs[pred] > self.respond_threshold:
            return self.tags[pred], probs_string
        elif probs[pred] > self.guess_threshold and self.use_guess_response:
            return self.best_guesses(probs), probs_string
        else:
            return None, probs_string

    def best_guesses(self, probs):
        """
        Calculates the best X tag guesses.

        :param probs: Pytorch Tensor
            Output probabilities
        :return: list of (tag, prob)
        """

        probs, indices = probs.sort(descending=True)
        responses = []
        prev_prob = 0
        for prob, idx in zip(probs, indices):
            gap = prev_prob - prob
            if gap/prev_prob > self.gap_ratio_threshold or len(responses) == self.max_guesses-1:
                break
            prev_prob = prob
            responses.append(self.tags[idx])
        return responses

    def get_prob(self, sentence, tag):
        """
        Gets the probability predicted by the model that the tag corresponds to the sentence.

        :param sentence: String
            Sentence to predict
        :param tag: String
            Tag that is possible output of the model
        :return:
            Probability that the tag matches the string
            The corresponding tag
        """

        x = self.to_input_array(sentence)
        nn_output = self.model(x)
        probs = torch.softmax(nn_output, dim=1)[0]
        _, pred = torch.max(nn_output, dim=1)
        return probs[self.tags.index(tag)], self.tags[pred]
