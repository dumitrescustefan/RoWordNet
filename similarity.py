from rowordnet import RoWordNet
from preprocessing.corpus import *


class Similarity(object):
    def __init__(self, wordnet, filename):
        """
            Initialize a similarity.

            Args:
                wordnet (WordNet): The wordnet ...?
                filename (str): The file where the corpus is located.

            Raises:
                TypeError: If any argument has incorrect type.
        """

        if not isinstance(wordnet, RoWordNet):
            raise TypeError("Argument 'wordnet' has incorrect type, expected Synset, got {}"
                            .format(type(wordnet).__name__))
        if not isinstance(filename, str):
            raise TypeError("Argument 'filename' has incorrect type, expected Synset, got {}"
                            .format(type(filename).__name__))

        self._wordnet = wordnet
        self._poses, self._lemmas = parse_corpus(filename, wordnet)

    def _overlap_context(self, synset, sentence):
        gloss = get_word_tokens(synset.definition)
        gloss = strip_stopwords(gloss)
        gloss = strip_punctuation(gloss)

        gloss = set(gloss)
        sentence = set(sentence)

        return len(gloss.intersection(sentence))

    def _simplified_lesk(self, literal, sentence):
        best_sense = None
        max_overlap = 0

        for synset in self._wordnet.synsets(literal):
            overlap = self._overlap_context(synset, sentence)

            for synset_id, relation in self._wordnet.outbound_relations(synset.id):
                if relation == 'hypernym':
                    overlap += self._overlap_context(synset_id, sentence)

            if overlap > max_overlap:
                max_overlap = overlap
                best_sense = synset

        return best_sense

    def lesk(self):
        for sentence in self._lemmas:
            for word in sentence:
                best_sense = self._simplified_lesk(word, sentence)
                print(best_sense)

