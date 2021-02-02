'''
    NUS CS4248 Assignment 1 - Objective 3 (n-gram Language Model)

    Class NgramLM for handling Objective 3


    Please use the following command for objective 3:
    OBJ3 path=STRING smooth=TYPE n_gram=INT k=FLOAT text=STRING next_word=STRING length=INT
    text: for generate_word(text), generate_next_word_probability(text, word), perplexity(text).
    next_word: for generate_next_word_probability(text, word)
    length: for generate_text(length)
    Please update the pattern_dict  accordingly.
    In the outputs, please mention which function gives what output. For instance,
    """
    Generated word: OUTPUT
    Probability of next word: OUTPUT
    Perplexity: OUTPUT
    Generated text: OUTPUT
    """ 
    If you implement any other type of smoothing, please mention in the write-up as to how run it
    as well - what is smooth=TYPE  value, does it require extra arguments like lambda, etc.?


'''
import random, math

class NgramLM(object):

    def __init__(self, n, k):
        '''
            Initialize your n-gram LM class

            Parameters:
                n (int) : order of the n-gram model
                k (float) : smoothing hyperparameter

        '''
        # Initialise other variables as necessary
        self.n = n
        self.k = k
        self.word_count_dict = {}
        self.vocabulary = set()
        self.ngrams = []

    def update_corpus(self, text):
        ''' Updates the n-grams corpus based on text. ADD to corpus'''
        
        pass


    def read_file(self, path):
        ''' Read the file and update the corpus  '''
        with open(path, encoding='utf-8', errors='ignore') as f:
            text = f.read()
        text = text.lower()
        self.update_corpus(text)


    def ngrams(self):
        ''' Returns ngrams of the text as list of pairs - [(sequence context, word)] '''
        # TODO Write your code here
        pass


    def add_padding(self):
        '''  Returns padded text '''
        # TODO Write your code here
        # Use '~' as your padding symbol just put it infront. don't pad end.
        # pad each sentence of the corpus.
        pass


    def get_vocabulary(self):
        ''' Returns the vocabulary as set of words '''
        # TODO Write your code here
        pass


    def get_next_word_probability(self, text, word):
        ''' Returns the probability of word appearing after specified text '''
        # TODO Write your code here
        pass


    def generate_word(self, text):
        '''
        Returns a random word based on the specified text and n-grams learned
        by the model
        '''
        # TODO Write your code here
        pass


    def generate_text(self, length):
        ''' Returns text of the specified number of words based on the learned model '''
        # MUST BE RANDOM> NOT DETERMINISTIC.
        # TODO Write your code here
        pass


    def perplexity(self, text):
        '''
        Returns the perplexity of text based on learned model

        Hint: To avoid numerical underflow, add logs instead of multiplying probabilities.
        Also handle the case when the LM assigns zero probabilities.
        '''
        # TODO Write your code here
        pass
