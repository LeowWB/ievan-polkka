from obj1_tokenizer import Tokenizer

a = Tokenizer('musketeers.txt',False)
print(a.get_frequent_words(20))
a.plot_word_frequency()