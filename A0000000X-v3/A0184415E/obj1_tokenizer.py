'''
    NUS CS4248 Assignment 1 - Objective 1 (Tokenization)

    Class Tokenizer for handling Objective 1
'''
import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords   # Requires NLTK in the include path.
import matplotlib.pyplot as plt     # Requires matplotlib to create plots.
import re
import math

STOPWORDS = stopwords.words('english') # type: list(str)
STOPWORDS = reversed(sorted(STOPWORDS,key=len)) # sort by reversed length to remove longer stopwords first

class Tokenizer:

    # don't change function signatures, but can add optional param
    def __init__(self, path, lowercase=False):
        with open(path, encoding='utf-8', errors='ignore') as f:
            self.text = f.read()
        if lowercase:
            self.text = self.text.lower()

    def tokenize(self):
        ''' Returns a set of word tokens '''
        tokens = Tokenizer.tokenize_text(self.text)
        self.tokens = tokens
        return tokens


    @staticmethod
    def tokenize_text(text):
        text = ' ' + text + ' ' # to ensure punctuation at start/end of text is removed correctly
        token_pattern = re.compile("(\w|'|-)+")
        tokens = list(filter(
            lambda token: token_pattern.match(token),
            re.split(r'\W*\s+\W*', text)
        ))
        return tokens


    # non-positive values of n will be treated as infinity (i.e. no limit)
    def get_frequent_words(self, n):
        ''' Returns the most frequent unigrams from the text '''
        tokens = self.tokenize()
        word_freqs = {}
        for token in tokens:
            word_freqs[token] = word_freqs.get(token, 0) + 1
        top_n = sorted(
            word_freqs.items(), key=lambda item: -item[1]
        )
        if n > 0:
            return top_n[:n]
        return top_n

    def plot_word_frequency(self):
        '''
        Plot relative frequency versus rank of word to check
        Zipf's law
        Relative frequency f = Number of times the word occurs /
                                Total number of word tokens
        Rank r = Index of the word according to word occurence list
        '''
        word_freqs = self.get_frequent_words(-1)
        freqs = [math.log(word_freq[1]/len(self.tokens), 10) for word_freq in word_freqs]
        ranks = [math.log(f, 10) for f in range(1,len(freqs)+1)]
        plt.scatter(ranks, freqs)
        plt.title('Graph of log of relative frequency against log of rank (base 10)')
        plt.show()


    def remove_stopwords(self):
        ''' Removes stopwords from the text corpus '''
        print('removing stopwords')
        stopword_regex = ''
        for stopword in STOPWORDS:
            stopword_regex += f'((?<!\w){stopword}(?!\w))|'
            stopword_regex += f'((?<!\w){stopword.capitalize()}(?!\w))|'
        stopword_regex = stopword_regex[:-1]
        self.text = re.sub(stopword_regex, '', self.text)
        return self.text
