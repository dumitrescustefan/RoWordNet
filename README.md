# RoWordNet

**RoWordNet stand for Romanian WordNet, a semantic network for the Romanian language**. RoWordNet mimics Princeton's WordNet, a large lexical database of English. 
The building block of a WordNet is the **synset** that expresses a unique concept. The synset (a synonym set) contains, as the name implies, a number of synonym words known as literals. The synset has more properties like a definition and links to other synsets. They also have a part-of-speech (pos) that groups them in four categories: nouns, verbs, adverbs and adjectives. Synsets are interlinked by **semantic relations** like hypernymy ("is-a"), meronymy ("is-part"), antonymy, and others. 

## Install

Simple, use python's pip:
```sh
pip install rowordnet
```

## Use

```python
import rowordnet
wn = rowordnet.wordnet()
```

For a demo on basic ops please see the Jupyter notebook here.
For a demo on more advanced ops please see the Jupyter notebook here.
For a demo on RoWordNet save/load ops please see the Jupyter notebook here.
For a demo on RoWordNet synset/relation creation and editing please see the Jupyter notebook here.

We present a few basic usage examples here:

##### Search for a word

As words are polysemous, searching for a word will likely yield more than one synset. A word is known as a literal in RoWordNet, and every synset has one or more literals that are synonyms.
```python
word = 'arbore'
synset_ids = wn.synsets(literal=word)
```
Eash synset has a unique ID, and most operations work with IDs. Here, ``wn.synsets(word)`` returns a list of synsets that contain word 'arbore' or None if the word is not found.

##### Print information about a synset

Calling ``wn.print_synset(id)`` prints all available info of a particular synset.

```python  
wn.print_synset(synset_id)
```

To get the actual Synset object, we simply call ``wn.synset(id)``:

```python
synset_object = wn.synset(synset_id)
```

To print any individual information, like its literals, definiton or ID, we simply call its properties:

```python
print("Print its literals (synonym words): {}".format(synset_object.literals))
print("Print its definition: {}".format(synset_object.definition))
print("Print its ID: {}".format(synset_object.id))
```
       
##### Synset access
    
The ``wn.synsets()`` function has two (optional) parameters, ``literal`` and ``pos``. If we specify a literal it will return all synset IDs that contain that literal. If we don't specify a literal, we will obtain a list of all existing synsets. The pos parameter filters by part of speech: NOUN, VERB, ADVERB or ADJECTIVE. The function returns a list of synset IDs.

```python    
synset_ids_all = wn.synsets() # get all synset IDs in RoWordNet
synset_ids_verbs = wn.synsets(pos=Synset.Pos.VERB) # get all verb synset IDs
synset_ids = wn.synsets(literal="cal", pos=Synset.Pos.NOUN) # get all synset IDs that contain word "cal" and are nouns
```


adj_synsets_id = wn.adjacent_synsets(synset_id, relation=relation)
t.b.d.


## Credits

