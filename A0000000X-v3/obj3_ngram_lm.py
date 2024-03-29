'''
    NUS CS4248 Assignment 1 - Objective 3 (n-gram Language Model)

    Class NgramLM for handling Objective 3




'''
import random, math, re
from obj1_tokenizer import Tokenizer

class NgramLM(object):

    def __init__(self, n, k, interpolation=False):
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
        self.total_words = 0
        self.total_sentences = 0
        self.interpolation = interpolation

        if interpolation:
            self.get_next_word_probability = self.get_next_word_probability_interpolation
            self.get_all_word_counts_given_context = self.get_all_word_counts_given_context_interpolation
        else:
            self.get_next_word_probability = self.get_next_word_probability_no_interpolation
            self.get_all_word_counts_given_context = self.get_all_word_counts_given_context_no_interpolation


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
            self.total_sentences += 1
            self.vocabulary = self.vocabulary.union(set(tokens))
            self.add_to_ngrams(tokens)
        self.vocabulary.remove('~') # we don't need this in vocab.


    def add_to_ngrams(self, tokens):
        '''
        Generates the list of ngrams from the list of tokens
        '''
        new_ngrams = []
        for i in range(1, len(tokens)):
            self.total_words += 1
            lower_bound = max([0, i-self.n+1])
            context = tokens[lower_bound:i]
            next_word = tokens[i]
            new_ngrams.append((tuple(context), next_word))
        self.ngrams += new_ngrams
        self.update_ngram_counts(new_ngrams)


    def update_ngram_counts(self, ngrams):
        '''
        Update the ngram counts; for each ngram, we also add versions of it with shorter context.
        Rationale: can be used for interpolation if original ngram is not found.
        '''
        for text_ngram in ngrams:
            # suppose text_ngram = (("i", "am"), "a"). then the following will be incremented:
            # (("i", "am"), "a"), (("am"), "a"), ((), "a")
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


    def generate_text(self, length):
        ''' Returns text of the specified number of words based on the learned model '''
        text = ""
        for i in range(length):
            text += self.generate_word(text) + " "
        return text


    def perplexity(self, text):
        '''
        Returns the perplexity of text based on learned model

        Hint: To avoid numerical underflow, add logs instead of multiplying probabilities.
        Also handle the case when the LM assigns zero probabilities.

        ASSUMPTION:
        We don't account for P(~|text), since we were explicitly told not to pad the text at the end.
        '''
        words = tuple(
            map(
                self.normalize_token,
                Tokenizer.tokenize_text(text)
            )
        )
        context = ''
        log_prob_sum = 0

        for word in words:
            prob = self.get_next_word_probability(context, word)
            if prob == 0:
                return float('nan')
            log_prob_sum += math.log(prob, 10)
            context += word + ' '
        
        total_prob = 10 ** log_prob_sum
        return total_prob ** (-1 / len(words))


    def normalize_token(self, token):
        '''
        Normalize by case folding. We don't do lemmatization and Penn Treebank, because that may
        give rise to strange-looking sentences in generate_text.
        '''
        return token.lower()

    def get_context_tokens(self, text):
        text_tokens = tuple(
            map(
                self.normalize_token,
                self.add_padding(Tokenizer.tokenize_text(text))
            )
        )
        num_elements_from_end = min(self.n - 1, len(text_tokens))
        if num_elements_from_end == 0:
            return ()
        else:
            return text_tokens[-num_elements_from_end:]

    def generate_word(self, text):
        '''
        Returns a random word based on the specified text and n-grams learned
        by the model. 
        '''
        counts = self.get_all_word_counts_given_context(text)
        total_counts = sum(counts.values())
        total_smoothed_counts = total_counts + (self.k * len(self.vocabulary))
        random_value = random.random() * total_smoothed_counts

        for word in self.vocabulary:
            # although the order of words isn't guaranteed to be constant, we don't have to shuffle
            # since we're making a random choice anyway (assume ordering of iteration over set is
            # independent of random_value)
            random_value -= counts[word]
            random_value -= self.k
            if random_value <= 0:
                return word
        
        assert False, "should not reach this point"

# FUNCTIONS WHEN THERE IS NO interpolation ===========================================================

    def get_next_word_probability_no_interpolation(self, text, word):
        '''
        Returns the probability of word appearing after specified text.
        NO interpolation
        '''
        word = self.normalize_token(word)
        if word not in self.vocabulary:
            return 0

        context = self.get_context_tokens(text)
        ngram = (context, word)
        numerator = self.ngram_counts.get(ngram, 0)
        
        if len(context) == 0:
            denominator = self.total_words
        elif context == ('~',):
            denominator = self.total_sentences
        else:
            denom_ngram = (context[:-1], context[-1])
            denominator = self.ngram_counts.get(denom_ngram, 0)

        numerator += self.k
        denominator += self.k * len(self.vocabulary)

        if denominator == 0:
            raise Exception("Division by 0 due to OOV")
        else:
            return numerator/denominator


    def get_all_word_counts_given_context_no_interpolation(self, text):
        '''
        Given a specific context, return a dict whose keys are V, and whose values are the
        counts of each word in the given context. 
        '''
        context = self.get_context_tokens(text)
        counts = {}
        for word in self.vocabulary:
            ngram = (context, word)
            counts[word] = self.ngram_counts.get(ngram, 0)
        return counts


# interpolation FUNCTIONS ============================================================================

    def get_all_word_counts_given_context_interpolation(self, text):
        '''
        Given a specific context, return a dict whose keys are V, and whose values are the
        (interpolated) "counts" of each word in the given context. 
        '''
        context = self.get_context_tokens(text)
        shortened_contexts = [context, context[1:], context[2:]]
        
        counts = {}
        for word in self.vocabulary:
            counts[word] = (
                self.ngram_counts.get((shortened_contexts[0], word), 0) * 0.8 +
                self.ngram_counts.get((shortened_contexts[1], word), 0) * 0.15 +
                self.ngram_counts.get((shortened_contexts[2], word), 0) * 0.05
            )
        return counts


    def get_next_word_probability_interpolation(self, text, word):
        '''
        Returns the probability of word appearing after specified text.
        USES interpolation.
        '''
        word = self.normalize_token(word)
        if word not in self.vocabulary:
            return 0

        counts = self.get_all_word_counts_given_context_interpolation(text)
        numerator = counts[word] + self.k
        denominator = sum(counts.values()) + (self.k * len(self.vocabulary))

        if denominator == 0:
            raise Exception("Division by 0 due to OOV")
        else:
            return numerator/denominator
      

# in case

    # def get_interpolation_context(self, text, word):
    #     '''
    #     interpolation until a context is found where (context, word) has a non-smoothed count > 0.
    #     '''
    #     text_tokens = self.add_padding(Tokenizer.tokenize_text(text))
    #     context_len = self.n - 1
    #     while context_len > 0:
    #         context = tuple(text_tokens[-context_len:])
    #         ngram = (context, word)
    #         if ngram in self.ngram_counts.keys():
    #             return context
    #         context_len -= 1
    #     return tuple()
  
