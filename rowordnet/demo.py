import .rowordnet
from .synset import Synset
from .rowordnet import intersection, merge, difference


def demo_basic_rowordnet_operations():
    print("\n\nThis demo shows the basic components and operations of the RoWordNet.\n"+"_"*70)
    # load rowordnet from internal resources
    wn = rowordnet.RoWordNet()
   
    # RoWordNet is composed of synsets linked together by semantic relations
    
    # the first operation is to search for a word. This will return one or more synsets.    
    word = 'arbore'
    synset_ids = wn.synsets(literal=word)
    print("\n\tTotal number of synsets containing literal '{}': {}".format(word, len(synset_ids)))
    print(synset_ids)
  
    # get a synset and print detailed information about it
    print("\n\tPrint detailed information about the first of these synsets:")
    synset_id = synset_ids[0]
    wn.print_synset(synset_id)
    
    # get the object itself
    print("\n\tGet the object itself by its id = {}, calling wn.synset():".format(synset_id))
    synset_object = wn.synset(synset_id)
    print("\t\t"+str(synset_object))
    
    print("\n\tGet the object itself by its id = {}, calling wn() directly:".format(synset_id))
    synset_object = wn(synset_id)
    print("\t\t"+str(synset_object))
    
    # print its literals, definition and id
    print("\n\tPrint its literals (synonym words): {}".format(synset_object.literals))
    print("\tPrint its definition: {}".format(synset_object.definition))
    print("\tPrint its id: {}".format(synset_object.id))
        
    # get all synsets as a list of synset IDs (list of strings)
    synsets_id = wn.synsets()
    print("\n\tTotal number of synsets: {} \n".format(len(synsets_id)))
    # example of iterating through synsets
    for synset_id in synsets_id:
        # get the synsets objects from the rowordnet by their IDs
        synset_object = wn(synset_id)
        # do something with the object
        pass

    # there are 4 types of parts of speech in RoWordNet : Nouns, Verbs, Adjectives and Adverbs
    # return all noun synsets
    synsets_id_nouns = wn.synsets(pos=Synset.Pos.NOUN)
    print("\tTotal number of noun synsets: {}".format(len(synsets_id_nouns)))
    # return all verb synsets
    synsets_id_verbs = wn.synsets(pos=Synset.Pos.VERB)
    print("\tTotal number of verb synsets: {}".format(len(synsets_id_verbs)))
    # return all adjective synsets
    synsets_id_adjectives = wn.synsets(pos=Synset.Pos.ADJECTIVE)
    print("\tTotal number of adjective synsets: {}".format(len(synsets_id_adjectives)))
    # return all adverb synsets
    synsets_id_adverbs = wn.synsets(pos=Synset.Pos.ADVERB)
    print("\tTotal number of adverb synsets: {}".format(len(synsets_id_adverbs)))
    
    # search for a word(here knows as a literal) in all noun synsets
    word = 'cal'
    print("\tSearch for all noun synsets that contain word/literal '{}'".format(word))    
    synset_ids = wn.synsets(literal=word, pos=Synset.Pos.NOUN)
    print("\t\tTotal number of noun synsets containing word/literal '{}' is {}, listed below:".format(word, len(synset_ids)))
    for synset_id in synset_ids:
        print("\t\t"+str(wn(synset_id)))
   
    # we continue with examples of navigating in the Wordnet 
    print("\n\tExamples of navigating the wordnet:")
    
    # get a synset
    synset_id = wn.synsets()[0]
    # get the path from a given synset to its root in hypermyn tree
    print("\tList of synset ids from synset with id '{}' up to its root in the hypermyn tree: ".format(synset_id))
    print("\t\t{}".format(wn.synset_to_hypernym_root(synset_id)))

    # print all outbound relations of a synset
    synset_id = wn.synsets("tren")[2]
    print("\n\tPrint all outbound relations of {}".format(wn(synset_id)))
    outbound_relations = wn.outbound_relations(synset_id)
    for outbound_relation in outbound_relations:
        target_synset_id = outbound_relation[0]        
        relation = outbound_relation[1]
        print("\t\tRelation [{}] to synset {}".format(relation, wn(target_synset_id)))
        
    # print all inbound relations of a synset, short syntax
    print("\n\tPrint all outbound relations of {}".format(wn(synset_id)))    
    for source_synset_id, relation in wn.inbound_relations(synset_id):
        print("\t\tRelation [{}] from synset {}".format(relation, wn(source_synset_id)))
        
    # get all relations of the same synset
    relations = wn.relations(synset_id)
    print("\tThe synset has {} total relations.".format(len(relations)))

    # get the shortest path between two synsets
    synset1_id = wn.synsets("cal")[2]
    synset2_id = wn.synsets("iepure")[0]    
    distance = wn.shortest_path(synset1_id, synset2_id)
    print("\n\tList of synsets containing the shortest path from synset with id '{}' to synset with id '{}': "
          .format(synset1_id, synset2_id))
    print("\t\t{}".format(distance))

    # get a new synset
    new_synset_id = wn.synsets("cal")[2]
    # travel the graph Breadth First 
    counter = 0
    print("\n\tTravel breadth-first through wordnet starting with synset '{}' (first 10 synsets) ..."
          .format(new_synset_id))
    for current_synset_id, relation, from_synset_id in wn.bfwalk(new_synset_id):
        counter += 1
        # bfwalk is a generator that yields, for each call, a BF step through wordnet 
        # you do actions with current_synset_id, relation, from_synset_id
        print("\t\t Step {}: from synset {}, with relation [{}] to synset {}".format(counter, from_synset_id, relation,
                                                                                     current_synset_id))
        if counter >= 10:
            break
        
    # get the lowest common ancestor in the hypernym tree
    synset1_id = wn.synsets("cal")[2]
    synset2_id = wn.synsets("iepure")[0]
    synset_id = wn.lowest_hypernym_common_ancestor(synset1_id, synset2_id)
    print("\n\tThe lowest common ancestor in the hypernym tree of synset: "
          "\n\t\t{} \n\t\t  and \n\t\t{} \n\t\t  is \n\t\t{}"
          .format(wn(synset1_id), wn(synset2_id), wn(synset_id)))
          
    # print all relation types existing in RoWordNet
    print("\n\tList all relation types existing in RoWordNet:")
    for relation in wn.relation_types: # this is a property
        print("\t\t{}".format(relation))


def demo_get_synonymy_antonymy():
    import itertools

    print("\n\nThis demo shows a bit more advanced series of ops.\n" + "_" * 70)

    # load from binary wordnet
    wn = rowordnet.RoWordNet()

    print("\n\tTask: We would like to extract a list of synonyms and antonyms from all the nouns in RoWordNet.")

    # get synonymy relations
    print("\n\tWe first extract synonyms directly from synsets. We list all noun synsets then iterate "
          "\n\tthrough them and create pairs from each synset.")

    synonyms = []
    synsets_id = wn.synsets()
    # for each synset, we create a list of synonyms between its literals
    for synset_id in synsets_id:
        # the literals object is a dict, but we need only the
        # actual literals (not senses)
        synset = wn(synset_id)
        literals = list(synset.literals)
        for i in range(len(literals)):
            for j in range(i+1, len(literals)):
                # append a tuple containing a pair of synonym literals
                synonyms.append((literals[i], literals[j]))

    # list a few synonyms
    print("\n\tList of the first 5 synonyms: ({} total synonym pairs extracted)".format(len(synonyms)))
    for i in range(5):
        print("\t\t {:>25} == {}".format(synonyms[i][0], synonyms[i][1]))

    # now, antonyms
    antonyms = []
    print("\n\tWe now want to extract antonyms. We look at all the antonymy relations and then for each "
          "\n\tpair of synsets in this relation we generate a cartesian product between their literals.")

    # extract all the antonymy relations from the graph and create a
    # list of synset pairs
    synset_pairs = []

    synsets_id = wn.synsets()  # extract all synsets
    for synset_id in synsets_id:
        synset = wn(synset_id)
        # extract the antonyms of a synset
        synset_outbound_id = wn.outbound_relations(synset.id)
        synset_antonyms_id = [synset_tuple[0] for synset_tuple in synset_outbound_id
                              if synset_tuple[1] == 'near_antonym']

        for synset_antonym_id in synset_antonyms_id:  # for each antonym synset
            synset_antonym = wn(synset_antonym_id)
            # if the antonymy pair doesn't already exists
            if (synset_antonym, synset) not in synset_pairs:
                # add the antonym tuple to the list
                synset_pairs.append((synset, synset_antonym))

    # for each synset pair extract its literals, so we now have a list of
    # pairs of literals
    literal_pairs = []
    for synset_pair in synset_pairs:
        # extract the literals of the first synset in the pair
        synset1_literals = list(synset_pair[0].literals)
        # extract the literals of the second synset in the pair
        synset2_literals = list(synset_pair[1].literals)
        # add a tuple containing the literals of each synset
        literal_pairs.append((synset1_literals, synset2_literals))

    # for each literals pair, we generate the cartesian product between them
    for literal_pair in literal_pairs:
        for antonym_tuple in itertools.product(literal_pair[0], literal_pair[1]):
            antonyms.append(antonym_tuple)

    # list a few antonyms
    print("\n\tList of the first 5 antonyms: ({} total antonym pairs extracted)".format(len(antonyms)))
    for i in range(5):
        print("\t\t {:>25} != {}".format(antonyms[i][0], antonyms[i][1]))


def demo_load_and_save_rowordnet():
    import time

    print("\n\nThis demo shows how to initialize, save and load a rowordnet object.\n" + "_"*70)
    
    # load internal rowordnet
    print("\n\t Loading from internal resources (binary)")
    start = time.perf_counter()
    wn = rowordnet.RoWordNet()
    print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))

    # save rowordnet to xml
    print("\n\t Saving the rowordnet in xml file")
    start = time.perf_counter()
    wn.save("rowordnet.xml", xml=True)
    print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))
    
    # load rowordnet from xml
    print("\n\t Load the rowordnet from xml file")
    start = time.perf_counter()
    wn.load("rowordnet.xml", xml=True)
    print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))
    
    # save rowordnet to binary
    print("\n\t Saving the rowordnet in binary file")
    start = time.perf_counter()
    wn.save("rowordnet.pickle")
    print("\t\t... done in {:.3f}s".format(time.perf_counter()-start))
    
    # load rowordnet from binary
    print("\n\t Load the rowordnet from binary file")
    start = time.perf_counter()
    wn.load("rowordnet.pickle")
    print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))


def demo_create_and_edit_synsets():
    print("\n\nThis demo shows how to create and edit synsets & relations.\n"+"_"*70)
        
    # create a synset( it's recommended to use the function 'generate_synset_id'
    # from the rowordnet class. See the function "demo_basic_rowordnet_operations'
    # for more details
    id = "my_id"
    synset = Synset(id)
    print("\n\tSynset with id '{}' has been created.".format(id))
    
    # printing the synset
    print("\n\tPrint this synset:")
    print(synset)

    # set a pos of type verb
    pos = Synset.Pos.VERB
    synset.pos = pos
    print("\tSynset's pos has been changed to '{}'". format(synset.pos))
    
    # add a literal
    literal = "tigru"
    sense = "1"
    synset.add_literal(literal=literal, sense=sense)
    print("\n\tA new literal '{}' with sense '{}' has been added to the synset with id '{}'"
          .format(literal, sense, synset.id))
    print("\tNumber of literals for synset with id '{}': {}".format(synset.id, len(synset.literals)))

    # remove a literal
    literal = "tigru"
    synset.remove_literal(literal=literal)
    print("\n\tThe literal '{}' has been removed from the synset with id '{}'".format(literal, synset.id))
    print("\tNumber of literals for synset with id '{}': {}".format(synset.id, len(synset.literals)))

    # add more literals at once
    print("\n\tAdding literals to a synset. Initially we create them:")
    literals = ['lup', 'vuple', 'caine']
    print("\tDirect addition of {} literals to synset with id '{}'".format(len(literals), synset.id))
    synset.literals = literals
    print("\tNumber of literals for synset with id '{}': {}".format(synset.id, len(synset.literals)))

    # add more senses at once 
    print("\n\tAdding senses to a synset's literals. Initially we create them:")
    literals_senses = ['1', '2', 'x']
    print("\tDirect addition of {} senses to synset with id '{}'".format(len(literals_senses), synset.id))
    synset.literals_senses = literals_senses
    print("\tNumber of senses for synset '{}': {}".format(synset.id, len(synset.literals_senses)))

    # set a definition
    definition = "Animal carnivor"
    synset.definition = definition
    print("\tSynset's defition has been changed to '{}'".format(synset.definition))

    # set a sumo
    sumo = "Animal"
    synset.sumo = sumo
    print("\tSynset's sumo has been changed to '{}'".format(synset.sumo))

    # set a sumotype
    sumotype = Synset.SumoType.INSTANCE
    synset.sumotype = sumotype
    print("\tSynset's sumotype has been changed to '{}'".format(synset.sumotype))          
          
    # generate a new id with default prefix and suffix
    wn = rowordnet.RoWordNet()
    id = wn.generate_synset_id()
    print("\n\tNew id '{}' generated with default prefix 'ENG30-' and suffix '-n'".format(id))
    # generate a new id with custom prefix and suffix
    prefix = 'ENG31-'
    suffix = '-v'
    new_id = wn.generate_synset_id(prefix=prefix, suffix=suffix)
    print("\tNew id '{}' generated with prefix '{}' and suffix '{}'".format(new_id, prefix, suffix))

    # create a synset with previous id
    synset = Synset(id)
    print("\n\tSynset with id '{}' has been created".format(synset.id))
    # add the synset to the rowordnet
    wn.add_synset(synset)
    print("\n\tAdded synset with id '{}' to the rowordnet".format(synset.id))

    # add a literal to synset
    literal = 'iepure'
    sense = '1'
    # get a synset
    synset_id = wn.synsets()[0]
    synset = wn(synset_id)
    # add a literal to the synset
    synset.add_literal(literal, sense)
    # tell the rowordnet that synsets's literals have been changed. This step is
    # necessary for a correct internal representation.
    wn.reindex_literals()
    print("\n\tAdded literal with literal '{}' and sense '{}' to the synset '{}'. "
          "Number of synsets containing literal '{}': {}"
          .format(literal, sense, synset.id, literal, len(wn.synsets(literal))))

    # remove the previous literal from synset.
    synset.remove_literal(literal)
    # again, we have to tell the rowordnet that synset's literals have been
    # changed.
    wn.reindex_literals()
    print("\tRemoved literal with literal '{}' from the synset '{}'. Number of synsets containing literal '{}': {}"
          .format(literal, synset.id, literal, len(wn.synsets(literal))))

    # generate a new synset
    prefix = 'ENG31-'
    suffix = '-n'
    new_id = wn.generate_synset_id(prefix, suffix)
    new_synset = Synset(new_id)
    wn.add_synset(new_synset)
    print("\n\tAdded new synset with id '{}' to the rowordnet".format(new_synset.id))

    # add a relation of type 'hypernym' from 'synset' to 'new_synset'
    relation = 'hypernym'
    wn.add_relation(synset.id, new_synset.id, relation)
    print("\n\tAdded '{}' relation from synset with id '{}' to synset with id '{}'"
          .format(relation, synset.id, new_synset.id))

    # remove relation of type 'hypernym' from 'synset' to 'new_synset'
    wn.remove_relation(synset.id, new_synset.id)
    print("\tRemoved relation from synset with id '{}' to synset with id '{}'".format(synset.id, new_synset.id))


def demo_operations_rowordnet():
    wn1 = rowordnet.RoWordNet()
    wn2 = rowordnet.RoWordNet()

    # add a new synset to the second wordnet
    new_synset_id = wn1.generate_synset_id()
    new_synset = Synset(new_synset_id)
    wn2.add_synset(new_synset)

    # modify a synset in the second wordnet
    synset_id = wn2.synsets("cal")[0]
    synset = wn2.synset(synset_id)
    synset.definition = "Definitie noua"

    # add a new relation in the second wordnet
    wn2.add_relation(new_synset_id, synset_id, "hypernym")

    # intersect two wordnets
    intersection_wn = intersection(wn1, wn2)
    print("Number of synsets in the intersect wordnet: {}\n".format(len(intersection_wn.synsets())))

    # merge two wordnets
    union_wn = merge(wn1, wn2)
    print("Numer of synsets in the union wordnet: {}\n".format(len(union_wn.synsets())))

    # different synsets/relations in the second wordnet
    diff_synsets, diff_relations = difference(wn1, wn2)
    print("Synsets that exists only in the second wordnet or that exists in both wordnets but are modified: {}"
          .format(diff_synsets))
    print("Relations that exists only in the second wordnet: {}".format(diff_relations))


if __name__ == '__main__':
    # rowordnet basic usage
    #demo_basic_rowordnet_operations()
    
    # rowordnet advanced usage
    #demo_get_synonymy_antonymy()
    
    # rowordnet editing
    #demo_load_and_save_rowordnet()
    #demo_create_and_edit_synsets()

    # rowordnet operations
    demo_operations_rowordnet()
    





