import sys
from tqdm import tqdm
from dependency import DependencyParse
from steps.parse_corpus import SingleSentenceParser


def head_to_tree(heads):
    # takes a list of dependency heads and returns each head's children as a dictionary
    heads = [h + 1 for h in heads]
    children = {}
    for i in range(0,len(heads)+1):
        children[i] = []
    for j in range(0,len(heads)):
        children[heads[j]].append(j+1)
    return children


def descendents(tree,i):
    # takes a dictionary and an index i and returns all descendents of the key at i
    if tree[i] == []:
        return [i]
    else:
        desc = [i]
        for c in tree[i]:
            desc+=(descendents(tree,c))
        return desc


def get_spans(tree):
    # takes a dictionary and returns a list of lists representing
    # constituents
    spans = []
    for i in tree:
        desc = descendents(tree,i)
        # we ignore one-word constituents
        if len(desc) > 1 and len(desc) < len(tree):
            spans.append([min(desc)-1,max(desc)])
    return spans
  

class BiaffineParser:

    def __init__(self):
        #self.parser = Predictor.from_path("https://allennlp.s3.amazonaws.com/models/biaffine-dependency-parser-ptb-2020.02.10.tar.gz")
        #self.parser = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/biaffine-dependency-parser-ptb-2020.04.06.tar.gz")
        #self.parser = pretrained.load_predictor("structured-prediction-biaffine-parser")
        self.parser = SingleSentenceParser()

    def __call__(self, sent):
        return self.get_spans(sent)

    def get_spans(self, sent):
        _, heads, _, _ = self.parser.parse(sent)
        spans = [tuple(span) for span in get_spans(head_to_tree(heads))]
        return spans

    def parse(self, sent):
        words, heads, deps, tags = self.parser.parse(sent)
        return DependencyParse(words, heads, deps, tags)

    def harvest_dependencies(self, sent, desired_deps):
        result = []
        words, heads, deps, _ = self.parser.parse(sent)
        for i in range(len(deps)):
            if deps[i] in desired_deps:
                result.append((words[i], words[heads[i]]))
        return result

    def parse_to_hierplane(self, sent):
        dparse = self.parse(sent)        
        return dparse.to_hierplane().to_json()


def main(in_file, out_file, desired_deps):
    parser = BiaffineParser()
    with open(in_file, 'r') as reader:
        with open(out_file, 'w') as writer:
            lines = list(reader)
            for i in tqdm(range(len(lines))):
                for (dependent, head) in parser.harvest_dependencies(lines[i], desired_deps):
                    writer.write('{} {}\n'.format(dependent, head))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3].split(','))
