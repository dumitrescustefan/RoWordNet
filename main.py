import wordnet
from synset import Synset


def intersection(wordnet_object_1, wordnet_object_2):
    return None


def union (wordnet_object_1, wordnet_object_2):
    return None


def merge (wordnet_object_1, wordnet_object_2):    
    return None


def complement (wordnet_object_1, wordnet_object_2):
    return None


def difference (wordnet_object_1, wordnet_object_2):
    return None


def demo_create_and_edit_synsets():
    print("\n\nThis demo shows how to create and edit synsets.\n"+"_"*70)

    # create a synset( it's recommended to use the function 'generate_synset_id'
    # from the wordnet class. See the function "demo_basic_wordnet_operations'
    # for more details
    id = "1"
    synset = Synset("my_id")
    print("\n\tSynset with id '{}' has been created.".format(id))
    
    # printing the synset
    print("\n\tPrinting this synset:")
    print(synset)

    # set a new id
    new_id = "2"
    synset.id = new_id
    print("\tSynset's id '{}' has been changed to '{}'"
          .format(id, synset.id))

    # set a pos of type verb
    pos = Synset.Pos.VERB
    synset.pos = pos
    print("\tSynset's pos has been changed to '{}'". format(synset.pos))

    # set a definition
    definition = "Animal carnivor"
    synset.definition = definition
    print("\tSynset's defition has been changed to '{}'"
          .format(synset.definition))

    # set a sumo
    sumo = "Animal"
    synset.sumo = sumo
    print("\tSynset's sumo has been changed to '{}'".format(synset.sumo))

    # set a sumotype
    sumotype = Synset.SumoType.INSTANCE
    synset.sumotype = sumotype
    print("\tSynset's sumotype has been changed to '{}'"
          .format(synset.sumotype))

    # add a literal
    word = "tigru"
    sense = "animal din savana"
    synset.add_literal(word=word, sense=sense)
    print("\n\tA new literal(word='{}', sense='{}') has been added to the "
          "synset with id '{}'".format(word, sense, synset.id))
    print("\tNumber of literals for synset with id '{}': {}"
          .format(synset.id, len(synset.literals)))

    # remove a literal
    word = "tigru"
    synset.remove_literal(word=word)
    print("\n\tThe literal(word='{}', sense='{}') has been removed from the "
          "synset with id '{}'".format(word, sense, synset.id))
    print("\tNumber of literals for synset with id '{}': {}"
          .format(synset.id, len(synset.literals)))

    # add more literals at once
    literals = {
                    'leu': '1',
                    'lup': '1.1',
                    'vulpe': 'x'
               }

    print("\n\tAdding literals to a synset. Initially we create them:")
    print(literals)
    print("\tDirect addition of {} literals to synset with id '{}'"
          .format(len(literals), synset.id))
    synset.literals = literals
    print("\tNumber of literals for synset with id '{}': {}"
          .format(synset.id, len(synset.literals)))


def demo_load_and_save_wordnet():
    import time

    print("\n\nThis demo shows how to initialize, "
          "save and load a wordnet object.\n" + "_"*70)
    # load internal wordnet
    print("\n\t Loading from internal resources")
    start = time.perf_counter()
    wn = wordnet.WordNet()
    print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))

    # save wordnet to xml
    print("\n\t Saving the wordnet in xml file")
    start = time.perf_counter()
    wn.save("resources/save_wn.xml")
    print("\t\t... done in {:.3f}s".format(time.perf_counter()-start))

    # load wordnet from xml
    print("\n\t Load the wordnet from xml file")
    start = time.perf_counter()
    wn.load("resources/save_wn.xml")
    print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))

    # save wordnet to binary
    print("\n\t Saving the wordnet in binary file")
    start = time.perf_counter()
    wn.save("resources/binary_wn.pck", xml=False)
    print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))

    # load wordnet to binary
    print("\n\t Load the wordnet from binary file")
    start = time.perf_counter()
    wn.load("resources/binary_wn.pck", xml=False)
    print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))


def demo_basic_wordnet_operations():
    print("\n\nThis demo shows how to work with synsets.\n"+"_"*70)
    # load from binary wordnet
    wn = wordnet.WordNet()
    
    # get all synsets
    synsets = wn.synsets()
    print("\n\tTotal number of synsets: {} \n".format(len(synsets)))
    # example of iterating through synsets
    for synset in wn.synsets():
        pass

    # return all noun synsets
    synsets_nouns = wn.synsets(pos=Synset.Pos.NOUN)
    print("\tTotal number of noun synsets: {}".format(len(synsets_nouns)))
    # return all verb synsets
    synsets_verbs = wn.synsets(pos=Synset.Pos.VERB)
    print("\tTotal number of verb synsets: {}".format(len(synsets_verbs)))
    # return all adjective synsets
    synsets_adjectives = wn.synsets(pos=Synset.Pos.ADJECTIVE)
    print("\tTotal number of adjective synsets: {}"
          .format(len(synsets_adjectives)))
    # return all adverb synsets
    synsets_adverbs = wn.synsets(pos=Synset.Pos.ADVERB)
    print("\tTotal number of adverb synsets: {}"
          .format(len(synsets_adverbs)))

    # search for a word in all synsets.
    # Returns an empty list if none is found.
    search_word = 'arbore'
    synset = wn.synsets(word=search_word)
    print("\n\tTotal number of synsets containing word '{}': {}\n"
          .format(search_word, len(synset)))

    # search for a word in all noun synsets
    search_word = 'cal'
    synset= wn.synsets(word=search_word, pos=Synset.Pos.NOUN)
    print("\tTotal number of noun synsets containing word '{}': {}"
          .format(search_word, len(synset)))

    # get the adjacent synsets of a synset.
    synset = wn.synsets(word='cal')[2]
    adj_synsets = wn.adj_synsets(synset.id)
    print("\n\tSynset with id '{}' has {} adjacent synsets"
          .format(synset.id, len(adj_synsets)))
    # get all adjacent synsets with a specific relation of this synset.
    relation = "hyponym"
    adj_synsets = wn.adj_synsets(synset.id, relation=relation)
    print("\tSynset with id '{}' has {} {} relations"
          .format(synset.id, len(adj_synsets), relation))

    # generate a new id with default prefix and suffix
    id = wn.generate_synset_id()
    print("\n\tNew id '{}' generated with default prefix 'ENG30-' "
          "and suffix '-n'".format(id))
    # generate a new id with custom prefix and suffix
    prefix = 'ENG31-'
    suffix = '-v'
    new_id = wn.generate_synset_id(prefix=prefix, suffix=suffix)
    print("\tNew id '{}' generated with prefix '{}' and suffix '{}'"
          .format(new_id, prefix, suffix))

    # create a synset with previous id
    synset = Synset(id)
    synset.save_changes()
    print("\n\tSynset with id '{}' has been created".format(synset.id))
    # add the synset to the wordnet
    print("\n\tAdded synset with id '{}' to the wordnet".format(synset.id))

    # add a literal to synset
    word = 'iepure'
    sense = '1'
    synset = wn.synsets()[0]
    synset.add_literal(word, sense)
    synset.save_changes()
    print("\n\tAdded literal with word '{}' and sense '{}' to "
          "the synset with id '{}'. Number of literals: {}"
          .format(word, sense, synset.id, len(synset.literals)))

    # remove the previous literal from synset. If no id for syset
    # is given then it will remove this literal from all synsets
    word = "iepure"
    synset = wn.synsets()[0]
    synset.remove_literal(word)
    synset.save_changes()
    print("\tRemoved literal with word '{}' from the synset with id '{}'. "
          "Number of literals: {}"
          .format(word, synset.id, len(synset.literals)))

    # generate a new synset
    prefix = 'ENG31-'
    suffix = '-n'
    new_id = wn.generate_synset_id(prefix, suffix)
    new_synset = Synset(new_id)
    wn.add_synset(new_synset)
    print("\n\tAdded new synset with id '{}' to the wordnet"
          .format(new_synset.id))

    # add a relation of type 'hypernym' from 'synset' to 'new_synset'
    relation = 'hypernym'
    wn.add_relation(synset.id, new_synset.id, relation)
    print("\n\tAdded '{}' relation from synset with id '{}' to synset "
          "with id '{}'".format(relation, synset.id, new_synset.id))

    # remove relation of type 'hypernym' from 'synset' to 'new_synset'
    wn.remove_relation(synset.id, new_synset.id)
    print("\tRemoved relation from synset with id '{}' to synset with "
          "id '{}'".format(synset.id, new_synset.id))

    # get a synset
    word = 'arbore'
    synset = wn.synsets(word=word)[0]
    # get the path from a given synset to root in hypermyn tree
    print("\n\tList of synsets from synset with id '{}' to root "
          "in hypermyn tree: ".format(synset.id))
    print("\t{}".format(wn.synset_to_root(synset.id)))

    # get two synsets
    synset1 = wn.synsets("cal")[2]
    synset2 = wn.synsets("iepure")[0]
    # get the shortest path between two synsets
    distance = wn.shortest_path(synset1.id, synset2.id)
    print("\n\tList of synsets containing the shortest path from synset with "
          "id '{}' to synset with id '{}': ".format(synset1.id, synset2.id))
    print("\t{}".format(distance))

    # get a new synset
    new_synset = wn.synsets("cal")[2]
    # travel the graph with bfs algorithm
    counter = 0
    print("\n\tTravelling breadth-first through wordnet (first 10 synsets)...")
    for current_synset, relation, from_synset in wn.bfwalk(new_synset.id):
        # bfwalk is a generator that yields, for each call, a BF step through wordnet
        # do actions with current_synset, relation, from_synset
        if counter > 10:
            break
        else:
            counter += 1
    print("\tNumber of synsets that have been travelled through "
          "in wordnet: {}".format(counter))

    # get the lowest common ancestor in the hypernym tree
    synset1 = wn.synsets("cal")[2]
    synset2 = wn.synsets("iepure")[0]
    x = wn.lowest_common_ancestor(synset1.id, synset2.id)
    print("\n\tLowest common ancestor in the hypernym tree of synset "
          "with id '{}' and synset with id '{}':"
          .format(synset1.id, synset2.id))
    print("\t{}".format(x))


def demo_get_synonymy_antonymy():
    import itertools

    print("\n\nThis demo shows how a bit more advanced series of ops.\n" + "_" * 70)

    # load from binary wordnet
    wn = wordnet.WordNet()

    print("\n\tTask: We would like to extract a list of synonyms and "
          "antonyms from all the nouns in WordNet.")

    # get synonymy relations
    print("\n\tWe first extract synonyms directly from synsets. "
          "We list all noun synsets then iterate \n\tthrough them and "
          "create pairs from each synset.")

    synonyms = []
    synsets = wn.synsets()
    for synset in synsets: # for each synset, we create a list of synonyms between its literals
        words = list(synset.literals.keys()) # the literals object is a dict, but we need only the actual words (not senses)
        for i in range(len(words)):
            for j in range(i+1,len(words)):
                synonyms.append((words[i],words[j])) # append a tuple containing a pair of synonym words

    # list a few synonyms
    print("\n\tList of the first 10 synonyms:")
    for i in range(10):
        print("\t\t {} == {}".format(synonyms[i][0],synonyms[i][1]))

    # now, antonyms
    antonyms = []
    print("\n\tWe now want to extract antonyms. We look at all the antonymy relations and then for each \n\tpair of synsets in this relation we generate a cartesian product between their literals.")

    # extract all the antonymy relations from the graph and create a list of synset pairs
    synset_pairs = []
        # aici o populam cu tupluri de id-uri de synset-uri in antonimie

    # for each synset pair extract its literals, so we now have a list of pairs of literals
    literal_pairs = []
    for synset_pair in synset_pairs:
        # adaugam literalii. stiu ca duplicam munca si e inutil acest pas, dar e pentru demo sa se inteleaga ordinea logica
        # practic in synset_pair[0] e id-ul primului synset, in [1] e al celui de-al doilea synset
        # in literal_pairs trebuie sa avem o lista de tupluri unde fiecare tuplu contine o lista de literali (string-uri, cum am facut mai sus cu list(syn_x.literals.keys), nu dict)
        pass

    # for each literals pair, we generate the cartesian product between them
    for literal_pair in literal_pairs:
        for antonym_tuple in itertools.product(literal_pair[0], literal_pair[1]):
            antonyms.append(antonym_tuple)

    # list a few antonyms
    print("\n\tList of the first 10 antonyms:")
    for i in range(10):
        print("\t\t {} == {}".format(antonyms[i][0], antonyms[i][1]))


def demo_operations_with_two_wordnets():
    pass


if __name__ == '__main__':
    demo_create_and_edit_synsets()
    demo_load_and_save_wordnet()
    demo_basic_wordnet_operations()
    #demo_get_synonymy_antonymy()

    # demo_operations_with_two_wordnets()

    




