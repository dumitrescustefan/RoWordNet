[![Build Status](https://travis-ci.org/dumitrescustefan/RoWordNet.svg?branch=master)](https://travis-ci.org/dumitrescustefan/RoWordNet)
[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/)

# RoWordNet

**RoWordNet stand for Romanian WordNet, a semantic network for the Romanian language**. RoWordNet mimics Princeton WordNet, a large lexical database of English. 
The building block of a WordNet is the **synset** that expresses a unique concept. The synset (a synonym set) contains, as the name implies, a number of synonym words known as literals. The synset has more properties like a definition and links to other synsets. They also have a part-of-speech (pos) that groups them in four categories: nouns, verbs, adverbs and adjectives. Synsets are interlinked by **semantic relations** like hypernymy ("is-a"), meronymy ("is-part"), antonymy, and others. 

## Install

Simple, use python's pip:
```sh
pip install rowordnet
```

RoWordNet has two dependencies: _networkx_ and _lxml_ which are automatically installed by pip.

## Intro

RoWordNet is, at its core, a directed graph (powered by networkx) with synset IDs as nodes and relations as edges. Synsets (objects) are kept as an ID:object indexed dictionary for O(1) access.

A **synset** has the following data, accessed as properties (others are present, but the following are most important): 
* id : the id(string) of this synset
* literals : a list of words(strings) representing a unique concept. These words are synonyms.
* definition : a longer description(string) of this synset
* pos : the part of speech of this synset (enum: Synset.Pos.NOUN, VERB, ADVERB, ADJECTIVE)
* sentiwn : a three-valued list indicating the SentiWN PNO (Positive, Negative, Objective) of this synset.

**Relations** are edges between synsets. Examples on how to list inbound/outbound relations given a synset and other graph operations are given in examples below.

____

* Demo on basic ops available as a [Jupyter notebook here](jupyter/basic_operations_wordnet.ipynb).
* Demo on more advanced ops available as a [Jupyter notebook here](jupyter/create_edit_synsets.ipynb).
* Demo on save/load ops available as a [Jupyter notebook here](jupyter/load_save_wordnet.ipynb).
* Demo on synset/relation creation and editing available as a [Jupyter notebook here](jupyter/synonym_antonym.ipynb).
____

## Basic Usage

```python
import rowordnet as rwn
wn = rwn.RoWordNet()
```

And you're good to go. We present a few basic usage examples here:

### Search for a word

As words are polysemous, searching for a word will likely yield more than one synset. A word is known as a literal in RoWordNet, and every synset has one or more literals that are synonyms.
```python
word = 'arbore'
synset_ids = wn.synsets(literal=word)
```
Eash synset has a unique ID, and most operations work with IDs. Here, ``wn.synsets(word)`` returns a list of synsets that contain word 'arbore' or an empty list if the word is not found. 

Please note that the Romanian WordNet also contains words (literals) that are actually expressions like "tren\_de\_marfă", and searching for "tren" will also find this synset.

### Get a synset

Calling ``wn.print_synset(id)`` prints all available info of a particular synset.

```python  
wn.print_synset(synset_id)
```

To get the actual Synset object, we simply call ``wn.synset(id)``, or ``wn(id)`` directly.

```python
synset_object = wn.synset(synset_id)
synset_object = wn(synset_id) # equivalent, shorter form
```

To print any individual information, like its literals, definiton or ID, we directly call the synset object's properties:

```python
print("Print its literals (synonym words): {}".format(synset_object.literals))
print("Print its definition: {}".format(synset_object.definition))
print("Print its ID: {}".format(synset_object.id))
```
       
### Synsets access
    
The ``wn.synsets()`` function has two (optional) parameters, ``literal`` and ``pos``. If we specify a literal it will return all synset IDs that contain that literal. If we don't specify a literal, we will obtain a list of all existing synsets. The pos parameter filters by part of speech: NOUN, VERB, ADVERB or ADJECTIVE. The function returns a list of synset IDs.

```python    
synset_ids_all = wn.synsets() # get all synset IDs in RoWordNet
synset_ids_verbs = wn.synsets(pos=Synset.Pos.VERB) # get all verb synset IDs
synset_ids = wn.synsets(literal="cal", pos=Synset.Pos.NOUN) # get all synset IDs that contain word "cal" and are nouns
```

For example we want to list all synsets containing word "cal":

```python
word = 'cal'
print("Search for all noun synsets that contain word/literal '{}'".format(word))    
synset_ids = wn.synsets(literal=word, pos=Synset.Pos.NOUN)
for synset_id in synset_ids:
    print(wn.synset(synset_id))
```
will output:
```
Search for all noun synsets that contain word/literal 'cal'
Synset(id='ENG30-03624767-n', literals=['cal'], definition='piesă la jocul de șah de forma unui cap de cal')
Synset(id='ENG30-03538037-n', literals=['cal'], definition='Nume dat unor aparate sau piese asemănătoare cu un cal :')
Synset(id='ENG30-02376918-n', literals=['cal'], definition='Masculul speciei Equus caballus')
````


### Relations access

Synsets are linked by relations (encoded as directed edges in a graph). A synset usually has outbound as well as inbound relation, To obtain the outbound relations of a synset use ``wn.outbound_relations()`` with the synset id as parameter. The result is a list of tuples like ``(synset_id, relation)`` encoding the target synset and the relation that starts from the current synset (given as parameter) to the target synset.

```python 
synset_id = wn.synsets("tren")[2] # select the third synset from all synsets containing word "tren"
print("\nPrint all outbound relations of {}".format(wn.synset(synset_id)))
    outbound_relations = wn.outbound_relations(synset_id)
    for outbound_relation in outbound_relations:
        target_synset_id = outbound_relation[0]        
        relation = outbound_relation[1]
        print("\tRelation [{}] to synset {}".format(relation,wn.synset(target_synset_id)))
```
Will output (amongst other relations):
```   
Print all outbound relations of Synset(id='ENG30-04468005-n', literals=['tren'], definition='Convoi de vagoane de cale ferată legate între și puse în mișcare de o locomotivă.')
    Relation [hypernym] to synset Synset(id='ENG30-04019101-n', literals=['transport_public'], definition='transportarea pasagerilor sau postei')
    Relation [hyponym] to synset Synset(id='ENG30-03394480-n', literals=['marfar', 'tren_de_marfă'], definition='tren format din vagoane de marfă')
    Relation [member_meronym] to synset Synset(id='ENG30-03684823-n', literals=['locomotivă', 'mașină'], definition='Vehicul motor de cale ferată, cu sursă de energie proprie sau străină, folosind pentru a remorca și a deplasa vagoanele.')
````
This means that from the current synset there are three relations pointing to other synsets: the first relation means that "tren" is-a (hypernym) "transport\_public"; the second relation is a hyponym, meaning that "marfar" is-a "tren"; the third member_meronym relation meaning that "locomotiva" is a part-of "tren".

The ``wn.inbound_relations()`` works identically but provides a list of _incoming_ relations to the synset provided as the function parameter, while ``wn.relations()`` provides allboth inbound and outbound relations to/from a synset (note: usually wn.relations() is provided as a convenience and is used for information/printing purposes as the returned tuple list looses directionality)
              


## Credits

Please consider citing the following paper as a thank you to the authors of the actual Romanian WordNet data:

```
Dan Tufiş, Verginica Barbu Mititelu, The Lexical Ontology for Romanian, in Nuria Gala, Reinhard Rapp, Nuria Bel-Enguix (Ed.), Language Production, Cognition, and the Lexicon, series Text, Speech and Language Technology, vol. 48, Springer, 2014, p. 491-504.
```
or in .bib format:

```
@InBook{DTVBMzock,
  title = "The Lexical Ontology for Romanian",
  author = "Tufiș, Dan and Barbu Mititelu, Verginica",booktitle = "Language Production, Cognition, and the Lexicon",
  editor = "Nuria Gala, Reinhard Rapp, Nuria Bel-Enguix",
  series = "Text, Speech and Language Technology",
  volume = "48",
  year = "2014",
  publisher = "Springer",
  pages = "491-504"}
```

.. and also to the autors of this [API](https://ieeexplore.ieee.org/abstract/document/8679089):

```
S. D. Dumitrescu, A. M. Avram, L. Morogan and S. Toma, "RoWordNet – A Python API for the Romanian WordNet," 2018 10th International Conference on Electronics, Computers and Artificial Intelligence (ECAI), Iasi, Romania, 2018, pp. 1-6.
```
or in .bib format:

```
@inproceedings{dumitrescu2018rowordnet,
  title={RoWordNet--A Python API for the Romanian WordNet},
  author={Dumitrescu, Stefan Daniel and Avram, Andrei Marius and Morogan, Luciana and Toma, Stefan-Adrian},
  booktitle={2018 10th International Conference on Electronics, Computers and Artificial Intelligence (ECAI)},
  pages={1--6},
  year={2018},
  organization={IEEE}
}
```

## Online query/visualizer for RoWordNet

Because there are many visitors that just want an **online interface to query RoWordNet**, please go to:

[http://dcl.bas.bg/bulnet/](http://dcl.bas.bg/bulnet/)

and choose in the upper right corner **PWN \& RoWN**. This interface provides pretty much the whole data available in this repo (after all it's a visualization interface) and it also includes mappings to Princeton's WordNet. Please note that this link is not associated with us in any way - we just use the same basic data and package it in an API for programatic use. By providing this link we're trying to help out people that just want to browse RoWordNet without having to code anything. 
