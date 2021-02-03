from obj3_ngram_lm import NgramLM
from pdb import set_trace

TEXT = ("I am a dwarf and I'm digging a hole! Diggy diggy hole! Digging a hole!\n" +
        "DWARF! HOLE! DIGGY DIGGY HOLE! DIGGY DIGGY HOLE! DIGGY DIGGY HOLE!")

ng = NgramLM(3, 0)
ng.update_corpus(TEXT)

assert ng.get_next_word_probability("i am a ", "dwarf") == 1
assert ng.get_next_word_probability("i are a ", "dwarf") == 1/3
assert ng.get_next_word_probability("hi","dwarf") == 2/26
assert ng.get_next_word_probability("i am a", "miner") == 0

set_trace()