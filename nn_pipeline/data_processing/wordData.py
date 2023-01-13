
import pandas as pd
import json


class WordData:
    """
    Class to init and store the word data.

    Reads the csv file with training data, stores the data and prepares the data for further processing.
    """

    def __init__(self, filename, nlp):
        """
        :param filename: String
            Path to .csv file

        :param raw_data:  List
            List of dicts containing "patterns", "responses" and "tags".

        :param all_words: List
            List of all unique pattern words

        :param tags: List
            List of all unique tags

        :param xy: tuple ([words], tag)
            Tuples containing ([words], tag) for each pattern
        """

        self.nlp = nlp
        self.csv = pd.read_csv(filename)
        self.raw_data = self.convert(self.csv)
        self.all_words, self.tags, self.xy, self.topics = self.init_words()

    def details(self):
        """
        Prints details of the data to the console.

        :return: None
        """
        print("Dataset:")
        print(" unique words:", len(self.all_words))
        print(" samples:", len(self.xy))
        print(" tags:", len(self.tags))
        print(" topics:", len(self.topics))
        print()

    def show(self):
        """
        Prints the data to the console.

        :return: None
        """
        for dic in self.raw_data:
            print("tag:", dic['tag'])
            print("patterns:")
            for pat in dic['patterns']:
                print("  ", pat)
            print("response:", dic['response'])
            print()

    def convert(self, csv):
        """
        Converts a pandas file to a structured dictionary.

        :param csv: pandas dataframe
            trainingdata.csv file
        :return: list of dicts containing "patterns" and "tags"
        """

        raw_data = []
        seen_tags = []

        for i in range(len(csv)):
            tag = csv['Tag'][i]
            pattern = csv['Input'][i]
            topic = csv['Topic'][i]

            if tag not in seen_tags:
                seen_tags.append(tag)
                dic = {
                    'topic': topic,
                    'tag': tag,
                    'patterns': [pattern],
                }
                raw_data.append(dic)
            else:
                for dic in raw_data:
                    if dic['tag'] == tag:
                        dic['patterns'].append(pattern)

        return raw_data

    def init_words(self):
        """
        Initializes the word data.

        Reads the raw data, tokenizes and stems the words using the NLP class.
        It then forms ngrams of size n_gram_size (initialized in main.py).

        :return:
            all_words: list of all unique pattern words
            tags:      list of all unique tags
            xy:        tuples containing ([words], tag) for each pattern
            topics:    list of all unique topics
        """

        all_words = []
        tags = []
        xy = []
        topics = []

        # print(json.dumps(self.raw_data, indent=4))

        for i, chat in enumerate(self.raw_data):
            tag = chat['tag']
            tags.append(tag)

            topic = chat['topic']
            topics.append(topic)

            for pattern in chat['patterns']:

                # remove punctuation, check spelling, tokenize, and lemmatize
                pattern = self.nlp.remove_punctuation(pattern)
                pattern = self.nlp.check_spelling(pattern)
                tokens = self.nlp.tokenize(pattern)
                tokens = self.nlp.lemmatize(tokens)

                # extend the list of encountered words
                all_words.extend(tokens)

                # save datapoint as tuple
                xy.append((tokens, tag, topic))

            print("Words from tag", i+1, "processed")
        print()

        all_words = sorted(set(all_words))
        tags = sorted(set(tags))
        topics = sorted(set(topics))

        return all_words, tags, xy, topics
