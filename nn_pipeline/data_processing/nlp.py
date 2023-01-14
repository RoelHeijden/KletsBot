
import spacy
import re
from spellchecker import SpellChecker


class NLP:
    """
    Natural language processing tools.

    Various functions for processing natural language.
    """

    def __init__(self):
        self.check_synonyms = True
        self.spell_checker = SpellChecker(distance=2)
        self.nlp = spacy.load("en_core_web_md")

    def remove_punctuation(self, sentence):
        sentence = sentence.lower()
        return re.sub(r'[^\w\s\'\?]', '', sentence)  # removes all but question marks and apostrophes

    def check_spelling(self, sentence):
        return sentence

    def tokenize(self, sentence):
        return self.nlp(sentence)

    def lemmatize(self, tokens):
        return [token.lemma_ for token in tokens]

    def get_synonyms(self, word):
        if self.check_synonyms:
            return [word]
        else:
            return [word]

