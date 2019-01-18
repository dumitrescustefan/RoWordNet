# in progress...
import os, sys, subprocess, time
import unittest

class Main_Tests(unittest.TestCase):
    def test_basic_ops(self):  
        
        from rowordnet import RoWordNet
        from synset import Synset
        
        wn = RoWordNet()
        word = 'arbore'
        synset_ids = wn.synsets(literal=word)
        print("\nTotal number of synsets containing literal '{}': {}".format(word, len(synset_ids)))
        self.assertTrue(len(synset_ids)>0)
        
        synsets_id_nouns = wn.synsets(pos=Synset.Pos.NOUN)
        print("\tTotal number of noun synsets: {}".format(len(synsets_id_nouns)))
        self.assertTrue(len(synsets_id_nouns)>0)
    
        synsets_id_verbs = wn.synsets(pos=Synset.Pos.VERB)
        print("\tTotal number of verb synsets: {}".format(len(synsets_id_verbs)))
        self.assertTrue(len(synsets_id_verbs)>0)
        
        synsets_id_adjectives = wn.synsets(pos=Synset.Pos.ADJECTIVE)
        print("\tTotal number of adjective synsets: {}".format(len(synsets_id_adjectives)))
        self.assertTrue(len(synsets_id_adjectives)>0)
        
        synsets_id_adverbs = wn.synsets(pos=Synset.Pos.ADVERB)
        print("\tTotal number of adverb synsets: {}".format(len(synsets_id_adverbs)))
        self.assertTrue(len(synsets_id_adverbs)>0)
    
        # search for a word(here knows as a literal) in all noun synsets
        word = 'cal'
        print("\tSearch for all noun synsets that contain word/literal '{}'".format(word))    
        synset_ids = wn.synsets(literal=word, pos=Synset.Pos.NOUN)
        print("\t\tTotal number of noun synsets containing word/literal '{}' is {}".format(word, len(synset_ids)))        
        self.assertTrue(len(synset_ids)>0)
        
    def test_io(self):       
        from rowordnet import RoWordNet
        
        # load internal rowordnet
        print("\nLoading from internal resources (binary)")
        start = time.perf_counter()
        wn = RoWordNet()
        print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))
        self.assertTrue(len(wn.synsets())>0)    

        # save rowordnet to xml
        print("\nSaving the rowordnet in xml file")
        start = time.perf_counter()
        wn.save("rowordnet.xml", xml=True)
        print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))
        self.assertTrue(len(wn.synsets())>0)
        
        # load rowordnet from xml
        print("\nLoad the rowordnet from xml file")
        start = time.perf_counter()
        wn.load("rowordnet.xml", xml=True)
        print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))
        self.assertTrue(len(wn.synsets())>0)
        
        # save rowordnet to binary
        print("\nSaving the rowordnet in binary file")
        start = time.perf_counter()
        wn.save("rowordnet.pickle")
        print("\t\t... done in {:.3f}s".format(time.perf_counter()-start))
        self.assertTrue(len(wn.synsets())>0)
        
        # load rowordnet from binary
        print("\nLoad the rowordnet from binary file")
        start = time.perf_counter()
        wn.load("rowordnet.pickle")
        print("\t\t... done in {:.3f}s".format(time.perf_counter() - start))
        self.assertTrue(len(wn.synsets())>0)
        
if __name__ == '__main__':
    """ Recreate bynary from xml
    from rowordnet import RoWordNet
    wn = RoWordNet(empty=True)
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
    """
    import os, sys; #
    print ("Current unit-test file location: "+os.path.realpath(__file__))
    location_of_rowordnet_package = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"rowordnet")
    print ("Adding "+location_of_rowordnet_package+" to path ...")
    sys.path.append(location_of_rowordnet_package)
    
    unittest.main()

    
"""
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
    





"""