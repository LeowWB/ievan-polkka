from obj3_ngram_lm import NgramLM
from pdb import set_trace

ng = NgramLM(4, 0, interpolation=True)
ng.read_file('musketeers.txt')

set_trace()
