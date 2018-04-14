import networkx as nx
from synset import Synset
import lxml.etree as et
from collections import defaultdict
import pickle
from queue import Queue
from exceptions import WordNetError


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
                list of str: A list containing all types of possible relations between synsets.
        """

        return self._relations_type

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
                    synset.literals = [literal.text for literal in element]
                    for literal in element:
                        synset.literals_senses.append(literal[0].text if literal is not None else "")
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
                    synset.sentiwn = [float(subelement.text) for subelement in element]

            self._synsets[synset.id] = synset

    def _load_from_binary(self, filename: str):
        wn = pickle.load(open(filename, "rb"))

        self._clean()

        self._relations_type = wn.relations_type

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
        pickle.dump(self, open(filename, "wb"))

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

        output = "Synset(id={!r}, pos={!r}, nonlexicalized={!r}, stamp={!r}, domain={!r}\n\t  definition={!r}" \
                 "\n\t  sumo={!r}, sumoType={!r}, sentiwn={!r})". \
            format(synset.id, synset.pos, synset.nonlexicalized, synset.stamp, synset.domain, synset.definition,
                   synset.sumo, synset.sumotype, synset.sentiwn)

        output += "\n\t  Literals:"
        for i in range(len(synset.literals)):
            output += "\n\t\t  {!r}:{!r}".format(synset.literals[i], synset.literals_senses[i])

        output += "\n"

        adj_synsets_id = list(self._graph.adj[synset_id].keys())
        output += "\t  Adjacent synsets: "
        output += str(adj_synsets_id)

        print(output)

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
        if relation not in self._relations_type:
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
                Synset: A synset representing the lowest common ancestor in the specified tree.
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
                if relation not in self._relations_type:
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


def intersection(wordnet_object_1, wordnet_object_2):
    return None


def union(wordnet_object_1, wordnet_object_2):
    return None


def merge(wordnet_object_1, wordnet_object_2):
    return None


def complement(wordnet_object_1, wordnet_object_2):
    return None


def difference(wordnet_object_1, wordnet_object_2):
    return None