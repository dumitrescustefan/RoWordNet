class WordNetError(Exception):
    def __init__(self, synid_not_in_wn=None, synid_ardy_in_wn=None, msg=None):
        if msg is not None:
            super(WordNetError, self).__init__(msg)
            return

        if synid_not_in_wn is not None:
            msg = "Synset with id '{}' is not in the wordnet".format(synid_not_in_wn)

        if synid_ardy_in_wn is not None:
            msg = "Synset with id '{} is already in the wordnet".format(synid_ardy_in_wn)

        super(WordNetError, self).__init__(msg)


def verify_type(name, type)