import networkx as nx
from synset import Synset
import lxml.etree as et
from collections import defaultdict
import pickle
from queue import Queue
from errors.exceptions import WordNetError


class WordNet(object):
    def __init__(self, filename=None, empty=False, xml=True):
        """
            Initialize a wordnet object.
            
            Args:
                filename (str, optional): File to load from. If filename==None,
                    load from internal resources. Defaults to None.
                empty (bool, optional): Set to True only if you want an empty
                    wordnet object (i.e. for manual wordnet editing
                    purposes, etc.) . Defaults to False.
                xml (bool, optional): If set to True the wordnet will be loaded
                    from an xml file. If set to False the wordnet will be
                    loaded from a binary file.

            Raises:
                TypeError: If any argument has incorrect type.
        """

        if not isinstance(filename, str) and filename is not None:
            raise TypeError("Argument 'filename' has incorrect type, "
                            "expected str, got {}"
                            .format(type(filename).__name__))
        if not isinstance(empty, bool):
            raise TypeError("Argument 'empty' has incorrect type, "
                            "expected bool, got {}"
                            .format(type(empty).__name__))
        if not isinstance(xml, bool):
            raise TypeError("Argument 'xml' has incorrect type, "
                            "expected bool, got {}".format(type(xml).__name__))

        self._clean()
        if empty:
            return

        if filename is None:
            self._load_from_binary("resources/binary_wn.pck")
            return

        if xml is True:
            self._load_from_xml(filename)
        elif xml is False:
            self._load_from_binary(filename)

    def _clean(self):
        self._graph = nx.DiGraph()
        self._synsets = {}
        self._literal2synset = defaultdict(list)
        self._relations_type = set()

    @property
    def relations_type(self):
        """
            Gets all types of possible relations between synsets.

            Returns:
                list of str: A list containing all types of
                    possible relations between synsets.
        """

        return self._relations_type

    def save(self, filename: str, xml: bool=True):
        """
            Save a wordnet object in a given file.
            
            Args:
                filename (str): The file where the wordnet will be saved.
                xml (bool, optional): If set to True, it will save in xml
                    format. If set to False it will save in binary format.
                    Defaults to True.

            Raises:
                TypeError: If any argument has incorrect type.
        """

        if not isinstance(filename, str):
            raise TypeError("Argument 'filename' has incorrect type, "
                            "expected str, got {}"
                            .format(type(filename).__name__))
        if not isinstance(xml, bool):
            raise TypeError("Argument 'xml' has incorrect type, "
                            "expected bool, got {}".format(type(xml).__name__))

        if xml is True:
            self._save_to_xml(filename)
        elif xml is False:
            self._save_to_binary(filename)

    def load(self, filename: str, xml: bool=True):
        """
            Load a wordnet object from a given file.

            Args:
                filename (str): The file from where wordnet
                    will be loaded.
                xml (bool, optional): If set to True, it will load from xml
                    format. If set to False, it will load from binary format.
                    Defaults to True.

            Raises:
                TypeError: If any argument has incorrect type.
        """

        if not isinstance(filename, str):
            raise TypeError("Argument 'filename' has incorrect type, "
                            "expected str, got {}"
                            .format(type(filename).__name__))
        if not isinstance(xml, bool):
            raise TypeError("Argument 'xml' has incorrect type, "
                            "expected bool, got {}".format(type(xml).__name__))

        if xml is True:
            self._load_from_xml(filename)
        elif xml is False:
            self._load_from_binary(filename)

    def _load_from_xml(self, filename):
        self._clean()

        root = et.parse(filename).getroot()

        for child in root:
            synset = Synset('0')

            for element in child:
                if element.tag == 'ID':
                    synset.id = element.text

                if element.tag == 'POS':
                    dic_chr2pos = {
                                    'n': Synset.Pos.NOUN,
                                    'v': Synset.Pos.VERB,
                                    'r': Synset.Pos.ADVERB,
                                    'a': Synset.Pos.ADJECTIVE
                                  }
                    pos = dic_chr2pos[element.text]
                    synset.pos = pos

                if element.tag == 'SYNONYM':
                    synset.literals = {literal.text: literal[0].text
                                       for literal in element}
                    for literal in element:
                        self._literal2synset[literal.text].append(synset.id)

                if element.tag == 'STAMP':
                    synset.stamp = element.text

                if element.tag == 'ILR':
                    self._relations_type.add(element[0].text)

                    self._graph.add_edge(synset.id, element.text,
                                         label=element[0].text)

                if element.tag == 'DEF':
                    synset.definition = element.text

                if element.tag == 'DOMAIN':
                    synset.domain = element.text

                if element.tag == 'SUMO':
                    synset.sumo = element.text
                    dic_chr2sumotype = {
                                        '+': Synset.SumoType.HYPERNYM,
                                        '=': Synset.SumoType.EQUIVALENT,
                                        '@': Synset.SumoType.INSTANCE,
                                        '[': Synset.SumoType.BRACKET,
                                        ':': Synset.SumoType.POINTS
                                       }
                    sumotype = dic_chr2sumotype[element[0].text]
                    synset.sumotype = sumotype

                if element.tag == 'SENTIWN':
                    synset.sentiwn = [float(subelement.text)
                                      for subelement in element]

            synset.add_wordnet(self)
            self._synsets[synset.id] = synset

    def _load_from_binary(self, filename):
        wn = pickle.load(open(filename, "rb"))

        self._clean()

        self._relations_type = wn.relations_type

        synsets = wn.synsets()

        for synset in synsets:
            adj_synsets = wn.adjacent_synsets(synset.id, show_relations=True)
            for adj_synset, relation in adj_synsets:
                self._graph.add_edge(synset.id, adj_synset.id, label=relation)

        for synset in synsets:
            self._synsets[synset.id] = synset

        for synset in synsets:
            for word in synset.literals.keys():
                self._literal2synset[word].append(synset.id)

    def _save_to_xml(self, filename):
        root = et.Element("ROWN")

        for synset in self._synsets.values():
            syn = et.SubElement(root, "SYNSET")

            et.SubElement(syn, "ID").text = synset.id

            et.SubElement(syn, "POS").text = str(synset.pos)

            synonym = et.SubElement(syn, "SYNONYM")
            for literal in synset.literals:
                lit = et.SubElement(synonym, "LITERAL")
                lit.text = literal
                et.SubElement(lit, "TYPE").text = "type"

            if synset.stamp is not None:
                et.SubElement(syn, "STAMP").text = synset.stamp

            if synset.id in self._graph.adj.keys():
                for target_node_id, edge_data in self._graph[synset.id].items():
                    ilr = et.SubElement(syn, "ILR")
                    ilr.text = target_node_id
                    et.SubElement(ilr, "TYPE").text = edge_data['label']
            if synset.definition is not None:
                et.SubElement(syn, "DEF").text = synset.definition

            if synset.domain is not None:
                et.SubElement(syn, "DOMAIN").text = synset.domain

            if synset.sumo is not None:
                sumo = et.SubElement(syn, "SUMO")
                sumo.text = synset.sumo
                et.SubElement(sumo, "TYPE").text = str(synset.sumotype)

            if synset.sentiwn is not None:
                sentiwn = et.SubElement(syn, "SENTIWN")
                et.SubElement(sentiwn, "P").text = str(synset.sentiwn[0])
                et.SubElement(sentiwn, "N").text = str(synset.sentiwn[1])
                et.SubElement(sentiwn, "O").text = str(synset.sentiwn[2])

        tree = et.ElementTree(root)
        tree.write(filename, encoding="utf-8", pretty_print=True)

    def _save_to_binary(self, filename):
        pickle.dump(self, open(filename, "wb"))

    def synsets(self, word: str=None, pos: Synset.Pos=None):
        """
            Get a list of synsets. If a word is given, only the synsets that
            contain that word will be selected. If a pos is given, only the
            synsets that have that pos will be selected.

            Args:
                word (str, optional): The word that synsets must contain.
                    Defaults to None.
                pos (Synset.Pos, optional): The type of pos that synsets
                    must have. Defaults to None.

            Returns:
                list of Synsets: A list containing the desired synsets. If no
                synset with the given word is found, it will return an
                empty list.

            Raises:
                TypeError: If any argument has incorrect type.

        """

        if word is None:
            synsets = list(self._synsets.values())
        else:
            if not isinstance(word, str):
                raise TypeError("Argument 'word' has incorrect type, "
                                "expected str, got {}"
                                .format(type(word).__name__))

            if word not in self._literal2synset:
                return []

            synsets_id = self._literal2synset[word]

            synsets = [self._synsets[synset_id] for synset_id in synsets_id]

        if pos is not None:
            if not isinstance(pos, Synset.Pos):
                raise TypeError("Argument 'pos' has incorrect type, "
                                "expected Synset.Pos, got {}"
                                .format(type(pos).__name__))

            synsets = [synset for synset in synsets if synset.pos == pos]

        return synsets

    def adjacent_synsets(self, synset_id: str, relation: str=None,
                    show_relations: bool=False):
        """
            Get the adjacent synsets of a synset with/without type of relations
            between synsets. You can't retrieve the types of relations if you
            specify a type of relation

            Args:
                synset_id (str): The id of the synset.
                relation (str): Type of relation we want.
                show_relations (str, optional): If set to True, it will show the
                    relations between synsets. Defaults to False.
            Returns:
                list of Synset: A list of synsets. If show_relations is set to
                True, returns a tuple of type (synset, relation).

            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given id in the
                    wordnet or if argument 'relation' has an incorrect value.

        """

        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, "
                            "expected str, got {}"
                            .format(type(synset_id).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset_id))
        if relation is not None and show_relations is not False:
            raise ValueError("Arguments 'relation' and 'show_relations'"
                             "can't be both valid")

        adj_synsets = []

        try:
            if show_relations is False:
                if relation is None:
                    adj_synsets = [self._synsets[adj_synset_id]
                                   for adj_synset_id in self._graph[synset_id]]
                else:
                    if not isinstance(relation, str):
                        raise TypeError(
                            "Argument 'relation' has incorrect type, "
                            "expected str, got {}"
                            .format(type(relation).__name__))
                    if relation not in self._relations_type:
                        raise WordNetError("Relation '{}' is not a correct "
                                           "relation".format(relation))
                    for adj_synset_id, data in self._graph.adj[synset_id].items():
                        if data['label'] == relation:
                            adj_synsets.append(self._synsets[adj_synset_id])
            else:
                if not isinstance(show_relations, bool):
                    raise TypeError("Argument 'show_relations' has incorrect "
                                    "type, expected bool, got {}"
                                    .format(type(show_relations).__name__))

                for adj_synset_id, data in self._graph.adj[synset_id].items():
                    adj_synsets.append((self._synsets[adj_synset_id],
                                        data['label']))
        except KeyError:
            return []

        return adj_synsets

    def synset(self, synset_id: str):
        """
            Get a synset, given its id.

            Args:
                synset_id (str): The id of the synset.

            Returns:
                Synset: The synset with the desired id. If no synset is found,
                the function will return None.

            Raises:
                TypeError: If any argument has incorrect type.
                WordNetError: If there's no synset with the given id in the
                    wordnet.
        """

        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, "
                            "expected str, got {}"
                            .format(type(synset_id).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset_id))

        return self._synsets[synset_id]

    def generate_synset_id(self, prefix='ENG30-', suffix='-n'):
        """
            Generate the first available id that starts with the given prefix
            and ends with the given suffix.

            Args:
                prefix (str, optional): The desired prefix. Defaults to 'ENG30-'
                suffix (str, optional): The desired suffix. Defaults to '-n'.

            Returns:
                str: The first available id that starts with the given prefix
                and ends with the given suffix.

            Raises:
                TypeError: If any argument has incorrect type.
        """

        if not isinstance(suffix, str):
            raise TypeError("Argument 'suffix' has incorrect type, "
                            "expected str, got {}"
                            .format(type(suffix).__name__))
        if not isinstance(prefix, str):
            raise TypeError("Argument 'prefix' has incorrect type, "
                            "expected str, got {}"
                            .format(type(prefix).__name__))

        matched = False
        maximum = 0

        for synset_id in self._synsets:
            if not synset_id.startswith(prefix):
                continue
            if not synset_id.endswith(suffix):
                continue

            matched = True

            synset_id = synset_id.replace(prefix, "")
            synset_id = synset_id.replace(suffix, "")

            if int(synset_id) > maximum:
                maximum = int(synset_id)

        if matched:
            return "{}{:08d}{}".format(prefix, maximum+1, suffix)
        else:
            return "{}{:08d}{}".format(prefix, 1, suffix)

    def add_synset(self, synset):
        """
            Add a synset to wordnet.

            Args:
                 synset (Synset): The synset to be added.

            Raises:
                TypeError: If any argument has incorrect type.
                WordNetError: If a synset with the given id is already in
                    the wordnet.
        """

        if not isinstance(synset, Synset):
            raise TypeError("Argument 'synset' has incorrect type, "
                            "expected Synset, got {}"
                            .format(type(synset).__name__))
        if synset.id in self._synsets:
            raise WordNetError("Synset with id '{}' is already in the wordnet"
                               .format(synset.id))

        self._graph.add_node(synset.id)
        self._synsets[synset.id] = synset
        synset.add_wordnet(self)
        for literal in synset.literals:
            self._literal2synset[literal].append(synset.id)

    def update_synset(self, synset):
        if synset.id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset.id))
        else:
            self._synsets[synset.id] = synset

            for word in synset.literals:
                self._literal2synset[word].append(synset.id)

    def add_relation(self, synset_id1, synset_id2, relation):
        """
            Add a new relation to the wordnet. Relation will always be from
            synset_id1 to synset_id2.

            Args:
                synset_id1 (str): Id of the first synset.
                synset_id2 (str): Id of the second synset.
                relation(str): Relation type between the synsets.

            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given ids in the
                    wordnet, if there's already a relation from the first
                    synset to the second synset or if the given relation has
                    an incorrect value.
        """

        if not isinstance(synset_id1, str):
            raise TypeError("Argument 'synset_id1' has incorrect type, "
                            "expected str, got {}"
                            .format(type(synset_id1).__name__))
        if not isinstance(synset_id2, str):
            raise TypeError("Argument 'synset_id2' has incorrect type, "
                            "expected str, got {}"
                            .format(type(synset_id2).__name__))
        if not isinstance(relation, str):
            raise TypeError("Argument 'relation' has incorrect type, "
                            "expected str, got {}"
                            .format(type(relation).__name__))
        if synset_id1 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset_id1))
        if synset_id2 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset_id2))
        if relation not in self._relations_type:
            raise WordNetError("Relation '{}' is not a correct relation"
                               .format(relation))
        if self._graph.has_edge(synset_id1, synset_id2):
            raise WordNetError("There's already a relation from the synset "
                               "with id '{}' to the synset with id '{}'"
                               .format(synset_id1, synset_id2))

        self._graph.add_edge(synset_id1, synset_id2, label=relation)

    def remove_relation(self, synset_id1, synset_id2):
        """
            Remove a relation between two synsets. Relation is always from the
            first synset to the second synset.

            Args:
                synset_id1 (str): Id of the first synset.
                synset_id2 (str): Id of the second synset.

            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given ids in the
                    wordnet or if there's no relation from the first synset to
                    the second synset.
        """

        if not isinstance(synset_id1, str):
            raise TypeError("Argument 'synset_id1' has incorrect type, "
                            "expected str, got {}"
                            .format(type(synset_id1).__name__))
        if not isinstance(synset_id2, str):
            raise TypeError("Argument 'synset_id2' has incorrect type, "
                            "expected str, got {}"
                            .format(type(synset_id2).__name__))
        if synset_id1 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset_id1))
        if synset_id2 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset_id2))
        if not self._graph.has_edge(synset_id1, synset_id2):
            raise WordNetError("There's no relation from the synset with id "
                               "'{}' to the synset with id '{}'"
                               .format(synset_id1, synset_id2))

        self._graph.remove_edge(synset_id1, synset_id2)

    def synset_to_root(self, synset_id, relation='hypernym'):
        """
            Get a list containing the path from the given synset to the root
            in a specified tree.

            Args:
                synset_id (str): Id of the synset.
                relation (str, optional): The type of relation from a child
                    to a parent.(there must not be a relation like 'hyponym'
                    or one that doesn't create a tree). Default to 'hypernym'.

            Returns:
                list: A list containing synset ids that create the path to the
                    root of the tree.

            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given id in the
                    wordnet or if the relation has an incorrect value.
        """

        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, "
                            "expected str, got {}"
                            .format(type(synset_id).__name__))
        if not isinstance(relation, str):
            raise TypeError("Argument 'relation' has incorrect type, "
                            "expected str, got {}"
                            .format(type(relation).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset_id))
        if relation not in self._relations_type:
            raise WordNetError("Relation '{}' is not a correct relation"
                               .format(relation))


        synset_id_ancestor = synset_id
        synset_id_to_root = [synset_id]

        while synset_id_ancestor is not None:
            adj_synsets_id = self._graph[synset_id_ancestor]

            synset_id_ancestor = None

            for adj_synset_id, adj_synset_data in adj_synsets_id.items():
                if adj_synset_data['label'] == relation:
                    synset_id_to_root.append(adj_synset_id)
                    synset_id_ancestor = adj_synset_id
                    break

        return synset_id_to_root

    def lowest_common_ancestor(self, synset_id1, synset_id2,
                               relation='hypernym'):
        """
            Find the lowest common ancestor of two synsets in a specified tree.

            Args:
                synset_id1 (str): Id of the first synset.
                synset_id2 (str): Id of the second synset.
                relation (str, optional): The type of relation from a child
                    to a parent.(there must not be a relation like 'hyponym'
                    or one that doesn't create a tree). Default to 'hypernym'.

            Returns:
                Synset: A synset representing the lowest common ancestor in the
                specified tree.

            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given ids in the
                    wordnet or if the relation has an incorrect value.
        """

        synset_id1_to_root = self.synset_to_root(synset_id1, relation)
        synset_id2_to_root = self.synset_to_root(synset_id2, relation)
                
        for synset_1 in synset_id1_to_root:
            for synset_2 in synset_id2_to_root:
                if synset_1 == synset_2:
                    lowest_common_ancestor = synset_1
                    return self._synsets[lowest_common_ancestor]

    def bfwalk(self, synset_id):
        """
            Travel the wordnet starting from a given synset.

            Args:
                synset_id (str): The id of the synset.

            Yields:
                Synset: The next synset in the wordnet.

            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given id in the
                    wordnet.
        """

        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, "
                            "expected str, got {}"
                            .format(type(synset_id).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset_id))

        queue = Queue()
        queue.put(synset_id)
        marked_synsets_id = [synset_id]
        from_synsets_rel = dict()
        from_synsets_rel[synset_id] = (None, None)

        while not queue.empty():
            cur_synset_id = queue.get()

            adj_synsets_id = self._graph.adj[cur_synset_id]

            for adj_synset_id, data in adj_synsets_id.items():
                if adj_synset_id not in marked_synsets_id:
                    marked_synsets_id.append(adj_synset_id)
                    queue.put(adj_synset_id)
                    from_synsets_rel[adj_synset_id] = (data['label'],
                                                       self._synsets[cur_synset_id])

            yield self._synsets[cur_synset_id], \
                from_synsets_rel[cur_synset_id][0], \
                from_synsets_rel[cur_synset_id][1]

            from_synsets_rel.pop(cur_synset_id)

    def shortest_path(self, synset_id1, synset_id2):
        """
            Get the shortest path from the first synset to the second synset.

            Args:
                synset_id1(str): Id of the first synset.
                synset_id2(str): Id of the second synset.

            Returns:
                list of str: A list of synset ids representing the path from
                the first synset to the second synset.

            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given ids in the
                    wordnet or if any relation has an incorrect value.
        """

        if not isinstance(synset_id1, str):
            raise TypeError("Argument 'synset_id1' has incorrect type, "
                            "expected str, got {}"
                            .format(type(synset_id1).__name__))
        if not isinstance(synset_id2, str):
            raise TypeError("Argument 'synset_id2' has incorrect type, "
                            "expected str, got {}"
                            .format(type(synset_id2).__name__))
        if synset_id1 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset_id1))
        if synset_id2 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet"
                               .format(synset_id2))

        return nx.shortest_path(self._graph, synset_id1, synset_id2)

    def similarity(self, word1: str, word2: str):
        pass




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
