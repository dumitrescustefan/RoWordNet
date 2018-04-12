import nltk
import nltk.corpus
from nltk.tokenize import RegexpTokenizer, sent_tokenize
from nltk.corpus import wordnet
import string


# input: a string containing one or more sentences (all in a single string)
# output: a list of sentences (strings)
def split_sentences(sentences):
    assert type(sentences) is str
    return sent_tokenize(sentences)


# input: list of words
# output: list of words without stopwords
def strip_stopwords(sentence):
    stopwords = nltk.corpus.stopwords.words('english') # stopword-urile din engleza?
    return [word for word in sentence if word.lower() not in stopwords]


# input: list of words
# output: list of words without stopwords
def strip_punctuation(sentence):
    all = []
    for word in sentence:
        all_punct = True
        for char in word:
            if char not in string.punctuation:
                all_punct = False
        if not all_punct:
            all.append(word)
    return all


# input: list of words
# output: list of lemmas and list of POSes
def lemmatize_and_pos(tokens):
    def get_wordnet_pos(pos_tag):
        if pos_tag[1].startswith('J'):
            return (pos_tag[0], wordnet.ADJ)
        elif pos_tag[1].startswith('V'):
            return (pos_tag[0], wordnet.VERB)
        elif pos_tag[1].startswith('N'):
            return (pos_tag[0], wordnet.NOUN)
        elif pos_tag[1].startswith('R'):
            return (pos_tag[0], wordnet.ADV)
        else:
            return (pos_tag[0], wordnet.NOUN)
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

    nltk_pos_tag_touples = nltk.pos_tag(tokens)

    pos_map = map(get_wordnet_pos, nltk_pos_tag_touples)
    lemmas = [lemmatizer.lemmatize(word, pos) for word, pos in pos_map]
    poses = [nltk_pos for word, nltk_pos in nltk_pos_tag_touples]

    return lemmas, poses


# input list of tokens, lemmas and posses
# output list of tokens, lemmas and posses without stopwords and punctuation #NOTE: this does not perform lemmatization and pos-tagging again
def lemmatize_and_pos_nostop_nopunct(original_tokens, original_lemmas, original_poses):
    tokens = []
    lemmas = []
    poses = []
    for i in range(len(original_tokens)):
        # first strip punctuation
        word = strip_punctuation([original_tokens[i]]) # hijack function so we don't duplicate code
        if not word == []: # this was not punctuation, so we continue
            # now check for stopwords
            stopword = strip_stopwords(word) # hijack this function as well, but now word is a list of a single string so we use it directly
            if not stopword == []: # we're ok, add the word
                tokens.append(original_tokens[i])
                lemmas.append(original_lemmas[i])
                poses.append(original_poses[i])
    return tokens, lemmas, poses


def is_english (s):
    return len(s) < 2*len(removeNonAscii(s))


def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)


def clean_string(sentence):
    sentence = sentence.replace(". . ","") # initial removal
    sentence = sentence.replace(". . ","") # for odd number of . points check
    sentence = sentence.replace("Ã‚Â","") # need to do this before removing all non-ascii
    sentence = removeNonAscii(sentence)
    return " ".join(sentence.split()) # remove multiple spaces


if __name__ == "__main__":
    nltk.download('wordnet')
    sentences = sent_tokenize("I like apples. No, I liked pineapples.")
    sentence_container = {"tokens": [], "poses": [], "lemmas": []}

    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        lemmas, poses = lemmatize_and_pos(tokens)

        sentence_container["tokens"].extend(tokens)
        sentence_container["lemmas"].extend(lemmas)
        sentence_container["poses"].extend(poses)

    print(sentence_container)




