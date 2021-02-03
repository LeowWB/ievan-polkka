from obj3_ngram_lm import NgramLM
from pdb import set_trace

mg = NgramLM(4, 0, interpolation=False)
mg.read_file('musketeers.txt')

set_trace()
