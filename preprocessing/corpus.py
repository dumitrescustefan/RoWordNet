from nltk.tokenize import sent_tokenize
import nltk
import string


def split_sentences(sentences):
    return sent_tokenize(sentences)


def word_tokens(sentence):
    return nltk.word_tokenize(sentence)


def strip_stopwords(tokens):
    """
        Removes the tokens that are stop words.

        Args:
            tokens (list of str): A list containing word tokens.
        Returns:
            list: A list containing the words that are not stop words.
    """
    stop_words = nltk.corpus.stopwords.words('romanian')
    return [word for word in tokens if word.lower() not in stop_words]


def strip_punctuation(tokens):
    """
        Removes the tokens that have punctuation marks.

        Args:
            tokens (list of str): A list containing word tokens.
        Returns:
            list: A list containing the words that don't containing
            punctuation marks
    """
    all = []
    for word in tokens:
        all_punct = True
        for char in word:
            if char not in string.punctuation:
                all_punct = False
        if not all_punct:
            all.append(word)
    return all


def get_lemmas(tokens):
    return tokens


def get_poses(tokens, wordnet):
    poses = []

    for token in tokens:
        synset = wordnet.synsets(token)[0]
        poses.append(synset.pos)

    return poses


def poses_and_lemmas(tokens, wordnet):
    tokens = strip_punctuation(tokens)
    tokens = strip_stopwords(tokens)

    lemmas = get_lemmas(tokens)
    poses = get_poses(tokens, wordnet)

    return poses, lemmas


def parse_corpus(filename, wordnet):
    with open(filename) as file:
        corpus = file.readlines()
        corpus = "".join(corpus)

    sentences = split_sentences(corpus)

    poses_list = []
    lemmas_list = []

    for sentence in sentences:
        tokens = word_tokens(sentence)

        poses, lemmas = poses_and_lemmas(tokens, wordnet)
        poses_list.append(poses)
        lemmas_list.append(lemmas)

    return poses_list, lemmas_list

























