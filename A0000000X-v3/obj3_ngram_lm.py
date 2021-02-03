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
import random, math, re
from obj1_tokenizer import Tokenizer

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
        self.ngram_counts = {}
        self.vocabulary = set()
        self.ngrams = []

    def update_corpus(self, text):
        ''' Updates the n-grams corpus based on text. ADD to corpus'''
        sentence_split_pattern = re.compile(r'[?!.]\s+')
        sentences = re.split(sentence_split_pattern, text)
        for sentence in sentences:
            tokens = self.add_padding(
                list(
                    map(
                        self.normalize_token,
                        Tokenizer.tokenize_text(sentence)
                    )
                )
            )
            self.vocabulary = self.vocabulary.union(set(tokens))
            self.add_to_ngrams(tokens)
        self.vocabulary.remove('~') # we don't need this in vocab.

    def add_to_ngrams(self, tokens):
        new_ngrams = []
        for i in range(1, len(tokens)):
            lower_bound = max([0, i-self.n+1])
            context = tokens[lower_bound:i]
            next_word = tokens[i]
            new_ngrams.append((tuple(context), next_word))
        self.ngrams += new_ngrams
        self.update_ngram_counts(new_ngrams)

    def update_ngram_counts(self, ngrams):
        '''
        Update the ngram counts; for each ngram, we also add versions of it with shorter context.
        Rationale: can be used for backoff if original ngram is not found.
        '''
        for text_ngram in ngrams:
            short_ngram = text_ngram
            while len(short_ngram[0]) > 0:
                self.increment_ngram_count(short_ngram)
                short_ngram = (short_ngram[0][1:], short_ngram[1])
            self.increment_ngram_count(short_ngram)

    def increment_ngram_count(self, ngram):
        self.ngram_counts[ngram] = self.ngram_counts.get(ngram, 0) + 1

    def read_file(self, path):
        ''' Read the file and update the corpus  '''
        with open(path, encoding='utf-8', errors='ignore') as f:
            text = f.read()
        self.update_corpus(text)


    def ngrams(self):
        ''' Returns ngrams of the text as list of pairs - [(sequence context, word)] '''
        return self.ngrams


    def add_padding(self, sentence_tokens=[]):
        '''  Returns padded text '''
        # Use '~' as your padding symbol just put it in front. don't pad end.
        # pad each sentence of the corpus.
        return ['~'] + sentence_tokens
        

    def get_vocabulary(self):
        ''' Returns the vocabulary as set of words '''
        return self.vocabulary


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

    def normalize_token(self, token):
        '''
        Normalize by case folding. We don't do lemmatization and Penn Treebank, because that may
        give rise to strange-looking sentences in generate_text.
        '''
        return token.lower()