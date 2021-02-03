from obj3_ngram_lm import NgramLM
from pdb import set_trace

TEXT = ("I am a dwarf and I'm digging a hole! Diggy diggy hole! Digging a hole! I am a dwarf and " +
        "I'm digging a hole! Diggy diggy hole! Digging a hole!\nDWARF! HOLE! DIGGY DIGGY HOLE! " +
        "DIGGY DIGGY HOLE! DIGGY DIGGY HOLE! DWARF! HOLE! DIGGY DIGGY HOLE! DIGGY DIGGY HOLE! " +
        "DIGGING A HOLE!")

ng = NgramLM(2, 0)
ng.update_corpus(TEXT)
set_trace()