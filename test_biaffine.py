import unittest

from biaffine import BiaffineParser


class TestBiaffine(unittest.TestCase):
    
    def test_get_spans(self):        
        parser = BiaffineParser()
        sent = "Short cuts make long delays."
        parse = parser.parse(sent)
        print(parse.words)
        print(parse.heads)
        print(parse.deps)
        print(parse.tags)
        amods = parser.harvest_dependencies(sent, "amod")
        print(amods)


if __name__ == "__main__":
    unittest.main()
