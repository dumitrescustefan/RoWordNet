import pickle
import networkx as nx
import lxml.etree as et
from collections import defaultdict
from queue import Queue

from .synset import Synset
from .exceptions import WordNetError


class RoWordNet(object):
    def __init__(self, filename: str = None, empty: bool = False, xml: bool = False):
        """
            Initialize a wordnet object.

            Args:
                filename (str, optional): File to load from. If filename==None, load from internal resources. Defaults
                    to None.
                empty (bool, optional): Set to True only if you want an empty wordnet object (i.e. for manual wordnet
                    editing purposes, etc.) . Defaults to False.
                xml (bool, optional): If set to True the wordnet will be loaded from an xml file. If set to False the
                    wordnet will be loaded from a binary file.
            Raises:
                TypeError: If any argument has incorrect type.
        """

        if not isinstance(filename, str) and filename is not None:
            raise TypeError("Argument 'filename' has incorrect type, expected str, got {}"
                            .format(type(filename).__name__))
        if not isinstance(empty, bool):
            raise TypeError("Argument 'empty' has incorrect type, expected bool, got {}".format(type(empty).__name__))
        if not isinstance(xml, bool):
            raise TypeError("Argument 'xml' has incorrect type, expected bool, got {}".format(type(xml).__name__))

        self._clean()
        if empty:
            return

        if filename is None:
            import pkg_resources
            path = "rowordnet.pickle"  # always use slash
            filepath = pkg_resources.resource_filename(__name__, path)
            self._load_from_binary(filepath)
            return

        if xml is True:
            self._load_from_xml(filename)
        elif xml is False:
            self._load_from_binary(filename)

    def _clean(self):
        self._graph = nx.DiGraph()
        self._synsets = {}
        self._literal2synset = defaultdict(list)
        self._relation_types = set()

    @property
    def relation_types(self):
        """
            Gets a set of all relation types existing in RoWordNet.
            Returns:
                set of str: A set containing all types of existing relations between synsets.
        """

        return self._relation_types

    def save(self, filename: str, xml: bool = False):
        """
            Save a wordnet object in a given file.

            Args:
                filename (str): The file where the wordnet will be saved.
                xml (bool, optional): If set to True, it will save in xml format. If set to False it will save in binary
                    format. Defaults to False.
            Raises:
                TypeError: If any argument has incorrect type.
        """

        if not isinstance(filename, str):
            raise TypeError("Argument 'filename' has incorrect type, expected str, got {}"
                            .format(type(filename).__name__))
        if not isinstance(xml, bool):
            raise TypeError("Argument 'xml' has incorrect type, expected bool, got {}".format(type(xml).__name__))

        if xml is True:
            self._save_to_xml(filename)
        elif xml is False:
            self._save_to_binary(filename)

    def load(self, filename: str, xml: bool = False):
        """
            Load a wordnet object from a given file.
            Args:
                filename (str): The file from where wordnet will be loaded.
                xml (bool, optional): If set to True, it will load from xml format. If set to False, it will load from
                    binary format. Defaults to False.
            Raises:
                TypeError: If any argument has incorrect type.
        """

        if not isinstance(filename, str):
            raise TypeError("Argument 'filename' has incorrect type, expected str, got {}"
                            .format(type(filename).__name__))
        if not isinstance(xml, bool):
            raise TypeError("Argument 'xml' has incorrect type, expected bool, got {}".format(type(xml).__name__))

        if xml is True:
            self._load_from_xml(filename)
        elif xml is False:
            self._load_from_binary(filename)

    def _load_from_xml(self, filename: str):
        self._clean()

        parser = et.XMLParser(encoding="utf-8")
        root = et.parse(filename, parser).getroot()

        for child in root:
            synset = None

            for element in child:
                if element.tag == 'ID':
                    synset = Synset(element.text)

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
                    try:
                        synset.literals = [literal.text for literal in element]
                    except TypeError as e:
                        print(synset.id)

                    literals_senses = []
                    for literal in element:
                        literals_senses.append(literal[0].text if literal[0].text is not None else "")
                    synset.literals_senses = literals_senses

                    for literal in synset.literals:
                        literal_parts = literal.split('_')
                        if len(literal_parts) > 1:
                            for literal_part in literal_parts:
                                if literal_part not in synset.literals:
                                    synset.add_literal(literal_part)

                    for literal in synset.literals:
                        self._literal2synset[literal].append(synset.id)

                if element.tag == 'STAMP':
                    synset.stamp = element.text

                if element.tag == 'ILR':
                    self._relation_types.add(element[0].text)

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
                    synset.sentiwn = [float(subelement.text) for subelement in element]

            self._synsets[synset.id] = synset

    def _load_from_binary(self, filename: str):
        with open(filename, "rb") as f:
            wn = pickle.load(f)

        self._clean()

        self._relation_types = wn.relation_types

        synsets_id = wn.synsets()

        for synset_id in synsets_id:
            adj_synsets_id = wn.outbound_relations(synset_id)
            for adj_synset_id, relation in adj_synsets_id:
                self._graph.add_edge(synset_id, adj_synset_id, label=relation)

        for synset_id in synsets_id:
            self._synsets[synset_id] = wn.synset(synset_id)

        for synset_id in synsets_id:
            synset = wn.synset(synset_id)
            for literal in synset.literals:
                self._literal2synset[literal].append(synset_id)

    def _save_to_xml(self, filename: str):
        root = et.Element("ROWN")

        for synset in self._synsets.values():
            syn = et.SubElement(root, "SYNSET")

            et.SubElement(syn, "ID").text = synset.id

            et.SubElement(syn, "POS").text = str(synset.pos)

            synonym = et.SubElement(syn, "SYNONYM")
            for literal in synset.literals:
                lit = et.SubElement(synonym, "LITERAL")
                lit.text = literal
                literal_index = synset.literals.index(literal)
                literal_sense = synset.literals_senses[literal_index]
                et.SubElement(lit, "SENSE").text = literal_sense

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

    def _save_to_binary(self, filename: str):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def synsets(self, literal: str = None, pos: Synset.Pos = None):
        """
            Get a list of synsets. If a literal is given, only the synsets that contain that literal will be selected.
            If a pos is given, only the synsets that have that pos will be selected.
            Args:
                literal (str, optional): The literal that synsets must contain. Defaults to None.
                pos (Synset.Pos, optional): The type of pos that synsets must have. Defaults to None.
            Returns:
                list of Synsets: A list containing the desired synsets. If no synset with the given word is found, it
                will return an empty list.
            Raises:
                TypeError: If any argument has incorrect type.
        """

        if literal is None:
            synsets_id = list(self._synsets.keys())
        else:
            if not isinstance(literal, str):
                raise TypeError("Argument 'literal' has incorrect type, expected str, got {}"
                                .format(type(literal).__name__))

            if literal not in self._literal2synset:
                return []

            synsets_id = self._literal2synset[literal]

        if pos is not None:
            if not isinstance(pos, Synset.Pos):
                raise TypeError("Argument 'pos' has incorrect type, expected Synset.Pos, got {}"
                                .format(type(pos).__name__))

            synsets_id = [synset_id for synset_id in synsets_id if self._synsets[synset_id].pos == pos]

        return synsets_id

    def print_synset(self, synset_id: str):
        """
            Fully prints a synset.

            Args:
                synset_id(str): Id of the synset.

            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given id in the wordnet.
        """

        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, expected str, got {}"
                            .format(type(synset_id).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id))

        synset = self.synset(synset_id)

        print("Synset: "
              "\n\t  id={}"
              "\n\t  pos={!r}"
              "\n\t  nonlexicalized={}"
              "\n\t  stamp={}"
              "\n\t  domain={}"
              "\n\t  definition={}" 
              "\n\t  sumo={} "
              "\n\t  sumoType={!r}"
              "\n\t  sentiwn={}".
              format(synset.id, synset.pos, synset.nonlexicalized, synset.stamp, synset.domain, synset.definition,
                     synset.sumo, synset.sumotype, synset.sentiwn))

        print("\t  Literals:")
        for i in range(len(synset.literals)):
            print("\t\t  {} - {}".format(synset.literals[i], synset.literals_senses[i]))

        outbound_relations = self.outbound_relations(synset_id)
        print("\t  Outbound relations: ")
        for out_synset_id, relation in outbound_relations:
            print("\t\t  {} - {}".format(out_synset_id, relation))

        inbound_relations = self.inbound_relations(synset_id)
        print("\t  Inbound relations: ")
        for in_synset_id, relation in inbound_relations:
            print("\t\t  {} - {}".format(in_synset_id, relation))

    def synset_exists(self, synset: Synset):
        if not isinstance(synset, Synset):
            raise TypeError("Argument 'synset' has incorrect type, expected Synset, got {}"
                            .format(type(synset).__name__))
        if synset.id not in self._synsets.keys():
            return False

        current_synset = self._synsets[synset.id]
        if current_synset != synset:
            return False

        return True

    def reindex_literals(self):
        """
            Reindex all literals to the synsets. This is used if the literals of a synset have been changed.
        """

        self._literal2synset.clear()
        for synset in self._synsets.values():
            for literal in synset.literals:
                self._literal2synset[literal].append(synset.id)

    def inbound_relations(self, synset_id: str):
        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, expected str, got {}"
                            .format(type(synset_id).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id))

        inbound_relations = []
        for synset_id_iter in self._graph.adj.keys():
            for adj_synset_id, data in self._graph.adj[synset_id_iter].items():
                if adj_synset_id == synset_id:
                    inbound_relations.append((synset_id_iter, data['label']))

        return inbound_relations

    def outbound_relations(self, synset_id: str):
        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, expected str, got {}"
                            .format(type(synset_id).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id))

        if synset_id not in self._graph.adj.keys():
            return []

        outbound_relations = []
        for adj_synset_id, data in self._graph.adj[synset_id].items():
            outbound_relations.append((adj_synset_id, data['label']))

        return outbound_relations

    def relations(self, synset_id: str):
        return self.outbound_relations(synset_id) + self.inbound_relations(synset_id)

    def relation_exists(self, synset_id1: str, synset_id2: str, relation: str):
        if not isinstance(synset_id1, str):
            raise TypeError("Argument 'synset_id1' has incorrect type, expected str, got {}"
                            .format(type(synset_id1).__name__))
        if not isinstance(synset_id2, str):
            raise TypeError("Argument 'synset_id2' has incorrect type, expected str, got {}"
                            .format(type(synset_id2).__name__))
        if not isinstance(relation, str):
            raise TypeError("Argument 'relation' has incorrect type, expected str, got {}"
                            .format(type(relation).__name__))
        if synset_id1 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id1))
        if synset_id2 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id2))
        if relation not in self._relation_types:
            raise WordNetError("Relation '{}' is not a correct relation".format(relation))

        for adj_synset_id, data in self._graph.adj[synset_id1].items():
            if adj_synset_id == synset_id2 and data['label'] == relation:
                return True

        return False

    def add_relation_type(self, relation_type: str):
        if not isinstance(relation_type, str):
            raise TypeError("Argument 'relation_type' has incorrect type, expected str, got {}"
                            .format(type(relation_type).__name__))
        if relation_type in self._relation_types:
            raise WordNetError("Relation type {} is already in the wordnet".format(relation_type))

        self._relation_types.add(relation_type)

    def __call__(self, synset_id: str):
        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, expected str, got {}"
                            .format(type(synset_id).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id))

        return self.synset(synset_id)
        
    def synset(self, synset_id: str):
        """
            Get a synset, given its id.
            Args:
                synset_id (str): The id of the synset.
            Returns:
                Synset: The synset with the desired id. If no synset is found, the function will return None.
            Raises:
                TypeError: If any argument has incorrect type.
                WordNetError: If there's no synset with the given id in the wordnet.
        """

        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, expected str, got {}"
                            .format(type(synset_id).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id))

        return self._synsets[synset_id]

    def generate_synset_id(self, prefix: str = 'ENG30-', suffix: str = '-n'):
        """
            Generate the first available id that starts with the given prefix and ends with the given suffix.
            Args:
                prefix (str, optional): The desired prefix. Defaults to 'ENG30-'
                suffix (str, optional): The desired suffix. Defaults to '-n'.
            Returns:
                str: The first available id that starts with the given prefix and ends with the given suffix.
            Raises:
                TypeError: If any argument has incorrect type.
        """

        if not isinstance(suffix, str):
            raise TypeError("Argument 'suffix' has incorrect type, expected str, got {}"
                            .format(type(suffix).__name__))
        if not isinstance(prefix, str):
            raise TypeError("Argument 'prefix' has incorrect type, expected str, got {}"
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
            return "{}{:08d}{}".format(prefix, maximum + 1, suffix)
        else:
            return "{}{:08d}{}".format(prefix, 1, suffix)

    def add_synset(self, synset: Synset):
        """
            Add a synset to wordnet.
            Args:
                 synset (Synset): The synset to be added.
            Raises:
                TypeError: If any argument has incorrect type.
                WordNetError: If a synset with the given id is already in the wordnet.
        """

        if not isinstance(synset, Synset):
            raise TypeError("Argument 'synset' has incorrect type, expected Synset, got {}"
                            .format(type(synset).__name__))
        if synset.id in self._synsets:
            raise WordNetError("Synset with id '{}' is already in the wordnet".format(synset.id))

        self._graph.add_node(synset.id)
        self._synsets[synset.id] = synset
        for literal in synset.literals:
            self._literal2synset[literal].append(synset.id)

    def add_relation(self, synset_id1: str, synset_id2: str, relation: str):
        """
            Add a new relation to the wordnet. Relation will always be from
            synset_id1 to synset_id2.
            Args:
                synset_id1 (str): Id of the first synset.
                synset_id2 (str): Id of the second synset.
                relation(str): Relation type between the synsets.
            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given ids in the wordnet, if there's already a relation from
                    the first synset to the second synset or if the given relation has an incorrect value.
        """

        if not isinstance(synset_id1, str):
            raise TypeError("Argument 'synset_id1' has incorrect type, expected str, got {}"
                            .format(type(synset_id1).__name__))
        if not isinstance(synset_id2, str):
            raise TypeError("Argument 'synset_id2' has incorrect type, expected str, got {}"
                            .format(type(synset_id2).__name__))
        if not isinstance(relation, str):
            raise TypeError("Argument 'relation' has incorrect type, expected str, got {}"
                            .format(type(relation).__name__))
        if synset_id1 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id1))
        if synset_id2 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id2))
        if relation not in self._relation_types:
            raise WordNetError("Relation '{}' is not a correct relation".format(relation))
        if self._graph.has_edge(synset_id1, synset_id2):
            raise WordNetError("There's already a relation from the synset with id '{}' to the synset with id '{}'"
                               .format(synset_id1, synset_id2))

        self._graph.add_edge(synset_id1, synset_id2, label=relation)

    def remove_relation(self, synset_id1: str, synset_id2: str):
        """
            Remove a relation between two synsets. Relation is always from the first synset to the second synset.
            Args:
                synset_id1 (str): Id of the first synset.
                synset_id2 (str): Id of the second synset.
            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given ids in the wordnet or if there's no relation from the
                    first synset to the second synset.
        """

        if not isinstance(synset_id1, str):
            raise TypeError("Argument 'synset_id1' has incorrect type, expected str, got {}"
                            .format(type(synset_id1).__name__))
        if not isinstance(synset_id2, str):
            raise TypeError("Argument 'synset_id2' has incorrect type, expected str, got {}"
                            .format(type(synset_id2).__name__))
        if synset_id1 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id1))
        if synset_id2 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id2))
        if not self._graph.has_edge(synset_id1, synset_id2):
            raise WordNetError("There's no relation from the synset with id '{}' to the synset with id '{}'"
                               .format(synset_id1, synset_id2))

        self._graph.remove_edge(synset_id1, synset_id2)

    def synset_to_hypernym_root(self, synset_id: str):
        """
            Get a list containing the path from the given synset to the root in a specified tree.
            Args:
                synset_id (str): Id of the synset.
            Returns:
                list: A list containing synset ids that create the path to the root of the tree.
            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given id in the wordnet.
        """

        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, expected str, got {}"
                            .format(type(synset_id).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id))

        synset_id_ancestor = synset_id
        synset_id_to_root = [synset_id]

        while synset_id_ancestor is not None:
            adj_synsets_id = self._graph[synset_id_ancestor]

            synset_id_ancestor = None

            for adj_synset_id, adj_synset_data in adj_synsets_id.items():
                if adj_synset_data['label'] == 'hypernym':
                    synset_id_to_root.append(adj_synset_id)
                    synset_id_ancestor = adj_synset_id
                    break

        return synset_id_to_root

    def lowest_hypernym_common_ancestor(self, synset_id1: str, synset_id2: str):
        """
            Find the lowest common ancestor of two synsets in a specified tree.
            Args:
                synset_id1 (str): Id of the first synset.
                synset_id2 (str): Id of the second synset.
            Returns:
                str: A synset representing the lowest common ancestor in the specified tree.
            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given ids in the wordnet.value.
        """

        synset_id1_to_root = self.synset_to_hypernym_root(synset_id1)
        synset_id2_to_root = self.synset_to_hypernym_root(synset_id2)

        for synset_1 in synset_id1_to_root:
            for synset_2 in synset_id2_to_root:
                if synset_1 == synset_2:
                    lowest_common_ancestor = synset_1
                    return lowest_common_ancestor

    def bfwalk(self, synset_id: str):
        """
            Travel the wordnet starting from a given synset.
            Args:
                synset_id (str): The id of the synset.
            Yields:
                Synset: The next synset in the wordnet.
            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given id in the wordnet.
        """

        if not isinstance(synset_id, str):
            raise TypeError("Argument 'synset_id' has incorrect type, expected str, got {}"
                            .format(type(synset_id).__name__))
        if synset_id not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id))

        queue = Queue()
        marked_synsets_id = [synset_id]
        from_synsets_rel = dict()

        for adj_synset_id, data in self._graph.adj[synset_id].items():
            from_synsets_rel[adj_synset_id] = (data['label'], synset_id)
            queue.put(adj_synset_id)
            marked_synsets_id.append(adj_synset_id)

        while not queue.empty():
            cur_synset_id = queue.get()

            adj_synsets_id = self._graph.adj[cur_synset_id]

            for adj_synset_id, data in adj_synsets_id.items():
                if adj_synset_id not in marked_synsets_id:
                    marked_synsets_id.append(adj_synset_id)
                    queue.put(adj_synset_id)
                    from_synsets_rel[adj_synset_id] = (data['label'], cur_synset_id)

            yield cur_synset_id, from_synsets_rel[cur_synset_id][0], from_synsets_rel[cur_synset_id][1]

            from_synsets_rel.pop(cur_synset_id)

    def shortest_path(self, synset_id1: str, synset_id2: str, relations: set = None):
        """
            Get the shortest path from the first synset to the second synset.
            Args:
                synset_id1 (str): Id of the first synset.
                synset_id2 (str): Id of the second synset.
                relations (list of str): The allowed relations in the shortest path algorithm.
            Returns:
                list of str: A list of synset ids representing the path from
                the first synset to the second synset.
            Raises:
                TypeError: If any argument has incorrect type.
                WordNerError: If there's no synset with the given ids in the wordnet or if any relation has an incorrect
                    value.
        """

        if not isinstance(synset_id1, str):
            raise TypeError("Argument 'synset_id1' has incorrect type, expected str, got {}"
                            .format(type(synset_id1).__name__))
        if not isinstance(synset_id2, str):
            raise TypeError("Argument 'synset_id2' has incorrect type, expected str, got {}"
                            .format(type(synset_id2).__name__))
        if synset_id1 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id1))
        if synset_id2 not in self._synsets:
            raise WordNetError("Synset with id '{}' is not in the wordnet".format(synset_id2))

        if relations is None:
            return nx.shortest_path(self._graph, synset_id1, synset_id2)
        else:
            if not isinstance(relations, set):
                raise TypeError("Argument 'relations' has incorrect type, expected set, got {}"
                                .format(type(relations).__name__))

            for relation in relations:
                if not isinstance(relation, str):
                    raise TypeError("Argument 'relation - relations' has incorrect type, expected str, got {}"
                                    .format(type(relation).__name__))
                if relation not in self._relation_types:
                    raise WordNetError("Relation '{}' is not a correct relation".format(relation))

            queue = Queue()
            queue.put(synset_id1)
            from_synset_id = {}
            marked_synset_ids = [synset_id1]
            found = False

            while not queue.empty() and not found:
                cur_synset_id = queue.get()

                for adj_synset_id, data in self._graph.adj[cur_synset_id].items():
                    if data['label'] in relations and adj_synset_id not in marked_synset_ids:
                        from_synset_id[adj_synset_id] = cur_synset_id
                        queue.put(adj_synset_id)
                        marked_synset_ids.append(adj_synset_id)

                        if adj_synset_id == synset_id2:
                            found = True

            shortest_path_list = [synset_id2]
            cur_synset_id = synset_id2

            while not cur_synset_id == synset_id1:
                cur_synset_id = from_synset_id[cur_synset_id]
                shortest_path_list.append(cur_synset_id)

            shortest_path_list.reverse()
            return shortest_path_list


def intersection(wordnet_1, wordnet_2):
    if not isinstance(wordnet_1, RoWordNet):
        raise TypeError("Argument 'wordnet_1' has incorrect type, expected RoWordNet, got {}"
                        .format(type(wordnet_1).__name__))
    if not isinstance(wordnet_2, RoWordNet):
        raise TypeError("Argument 'wordnet_2' has incorrect type, expected RoWordNet, got {}"
                        .format(type(wordnet_2).__name__))

    intersection_wordnet = RoWordNet(empty=True)

    for synset_id in wordnet_1.synsets():
        synset = wordnet_1.synset(synset_id)
        if wordnet_2.synset_exists(synset):
            intersection_wordnet.add_synset(synset)

    relations_type_wn1 = wordnet_1.relation_types
    relations_type_wn2 = wordnet_2.relation_types

    for relation_type_wn1 in relations_type_wn1:
        for relation_type_wn2 in relations_type_wn2:
            if relation_type_wn1 == relation_type_wn2:
                intersection_wordnet.add_relation_type(relation_type_wn1)
                break

    for synset_id in wordnet_1.synsets():
        relations_wn1 = wordnet_1.outbound_relations(synset_id)
        for relation_wn1 in relations_wn1:
            try:
                intersection_wordnet.add_relation(synset_id, relation_wn1[0], relation_wn1[1])
            except WordNetError:
                pass

    return intersection_wordnet


def merge(wordnet_1: RoWordNet, wordnet_2: RoWordNet):
    if not isinstance(wordnet_1, RoWordNet):
        raise TypeError("Argument 'wordnet_1' has incorrect type, expected RoWordNet, got {}"
                        .format(type(wordnet_1).__name__))
    if not isinstance(wordnet_2, RoWordNet):
        raise TypeError("Argument 'wordnet_2' has incorrect type, expected RoWordNet, got {}"
                        .format(type(wordnet_2).__name__))

    new_wordnet = RoWordNet(empty=True)

    # copying the second wordnet
    for synset_id in wordnet_2.synsets():
        synset = wordnet_2.synset(synset_id)
        new_wordnet.add_synset(synset)

    relations_type = wordnet_2.relation_types
    for relation_type in relations_type:
        new_wordnet.add_relation_type(relation_type)

    for synset_id in wordnet_2.synsets():
        relations = wordnet_2.outbound_relations(synset_id)
        for relation in relations:
            new_wordnet.add_relation(synset_id, relation[0], relation[1])

    # add the first wordnet
    relations_type = wordnet_1.relation_types
    for relation_type in relations_type:
        try:
            new_wordnet.add_relation_type(relation_type)
        except WordNetError:
            pass

    for synset_id in wordnet_1.synsets():
        try:
            synset = wordnet_1.synset(synset_id)
            new_wordnet.add_synset(synset)
        except WordNetError:
            pass

    for synset_id in wordnet_1.synsets():
        relations = wordnet_1.outbound_relations(synset_id)
        for relation in relations:
            try:
                new_wordnet.add_relation(synset_id, relation[0], relation[1])
            except WordNetError:
                pass

    return new_wordnet


def difference(wordnet_1, wordnet_2):
    if not isinstance(wordnet_1, RoWordNet):
        raise TypeError("Argument 'wordnet_1' has incorrect type, expected RoWordNet, got {}"
                        .format(type(wordnet_1).__name__))
    if not isinstance(wordnet_2, RoWordNet):
        raise TypeError("Argument 'wordnet_2' has incorrect type, expected RoWordNet, got {}"
                        .format(type(wordnet_2).__name__))

    diff_synsets = set()
    diff_relations = set()

    for synset_id in wordnet_2.synsets():
        try:
            synset1 = wordnet_1.synset(synset_id)
            synset2 = wordnet_2.synset(synset_id)
            if synset1 != synset2:
                diff_synsets.add(synset_id)
        except WordNetError:
            diff_synsets.add(synset_id)

    for synset_id in wordnet_2.synsets():
        relations = wordnet_2.outbound_relations(synset_id)
        for relation in relations:
            try:
                if not wordnet_1.relation_exists(synset_id, relation[0], relation[1]):
                    diff_relations.add((synset_id, relation[1], relation[0]))
            except WordNetError:
                diff_relations.add((synset_id, relation[1], relation[0]))

    return diff_synsets if len(diff_synsets) > 0 else None, diff_relations if len(diff_relations) > 0 else None

