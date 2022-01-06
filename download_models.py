import benepar
import nltk
benepar.download('benepar_en3')
nltk.download('punkt')

from berkeley import BerkeleyParser
from biaffine import BiaffineParser
from coref import AllenCoref

berkeley_parser = BerkeleyParser()
biaffine_parser = BiaffineParser()
allen_coref = AllenCoref()