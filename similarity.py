from wordnet import WordNet
from preprocessing.corpus import *
from math import log

# adaug commenturile si check-urile daca e bine


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

        if not isinstance(wordnet, WordNet):
            raise TypeError("Argument 'wordnet' has incorrect type, "
                            "expected Synset, got {}"
                            .format(type(wordnet).__name__))
        if not isinstance(filename, str):
            raise TypeError("Argument 'filename' has incorrect type, "
                            "expected Synset, got {}"
                            .format(type(filename).__name__))

        self._wordnet = wordnet
        self._poses, self._lemmas = parse_corpus(filename, wordnet)
        self._information_content = {}

    def _init_information_content(self):
        synsets = self._wordnet.synsets()
        self._information_content = {synset.id: 0 for synset in synsets}

    def _overlap_context(self, synset, sentence):
        gloss = get_word_tokens(synset.definition) # tokenizez definitie
        gloss = strip_stopwords(gloss) # sterg stop word-urile
        gloss = strip_punctuation(gloss) # sterg semnele de punctuatie

        gloss = set(gloss)
        sentence = set(sentence)

        return len(gloss.intersection(sentence)) # calculez intersectia

    def _simplified_lesk(self, word, sentence):
        best_sense = None
        max_overlap = 0

        for synset in self._wordnet.synsets(word): # iau fiecare synset ce contine cuv respectiv
            overlap = self._overlap_context(synset, sentence) # calculez overlapul

            if overlap > max_overlap: # salvez noul overlap
                max_overlap = overlap
                best_sense = synset

        return best_sense

    # in engleza se calculeaza overlapul si pentru hyponyms
    def lesk(self):
        self._init_information_content() # init inform cont al synset cu 0

        synsets = self._wordnet.synsets()
        synset_appearance_counter = {synset.id: 0 for synset in synsets} # init fiecare aparitie a syn cu 0
        word_counter = 0 # numarul de cuvinte din corpus lemmatizat

        for sentence in self._lemmas: # pentru ficare prop din lemmas
            for word in sentence: # pentru fiecare cuv din prop
                best_sense = self._simplified_lesk(word, sentence) # aleg cel mai bun synset
                synset_appearance_counter[best_sense.id] += 1 # aparitie creste cu 1
                word_counter += 1 # numarul de cuv creste cu 1

        # calculez info content al fiecarui cuvant ce a aparut in corpus
        for synset_id, counter in synset_appearance_counter.items():
            if not counter == 0:
                self._information_content[synset_id] = -log(counter/word_counter, 2)

    def resnik(self, synset_id1, synset_id2, relation="hypernym"):
        lca = self._wordnet.lowest_common_ancestor(synset_id1, synset_id2, relation)
        return self._information_content[lca.id]

    def jcn(self, synset_id1, synset_id2, relation="hypernym"):
        return (2*self.resnik(synset_id1, synset_id2, relation) -
                self._information_content[synset_id1] -
                self._information_content[synset_id2])

    def lin(self, synset_id1, synset_id2, relation="hypernym"):
        return (2*self.resnik(synset_id1, synset_id2, relation) /
                (self._information_content[synset_id1] +
                self._information_content[synset_id2]))

    def jcn_distance(self, synset_id1, synset_id2, relation="hypernym"):
        return (self._information_content[synset_id1] +
                self._information_content[synset_id2] -
                2*self.resnik(synset_id1, synset_id2))



