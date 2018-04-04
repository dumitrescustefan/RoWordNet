import os
import xml.etree.ElementTree as et
from components import Synset, Literal, Relation


def xml_read_synsets(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError('No such file: {}'.format(file_path))

    synsets = []

    root = et.parse(file_path).getroot()

    for child in root:
        synset = Synset()

        for element in child:
            if element.tag == 'ID':
                synset.id = element.text

            if element.tag == 'POS':
                type = Synset.str_to_pos(element.text)
                if type is None:
                    raise ValueError('Unidentified pos "{}" while reading synet with id {}'
                                     .format(element.text, synset.id))
                synset.pos = type

            if element.tag == 'SYNONYM':
                for subelement in element:
                    literal = Literal()
                    literal.literal = subelement.text
                    literal.sense = subelement[0].text
                    synset.literals.append(literal)

            if element.tag == 'STAMP':
                synset.stamp = element.text

            if element.tag == 'ILR':
                relation = Relation()
                relation.source_synet = synset.id
                relation.target_synet = element.text
                relation.relation = element[0].text
                synset.relations.append(relation)

            if element.tag == 'DEF':
                synset.definition = element.text

            if element.tag == 'DOMAIN':
                synset.domain = element.text

            if element.tag == 'SUMO':
                sumotype = Synset.str_to_sumo(element[0].text)
                if sumotype is None:
                    raise ValueError('Unidentified sumo type "{}" while reading synet with id {}'
                                     .format(element.text, synset.id))
                synset.sumo = element.text
                synset.sumotype = sumotype

            if element.tag == 'SENTIWN':
                synset.sentiwn_p = element[0].text
                synset.sentiwn_n = element[1].text
                synset.sentiwn_o = element[2].text

        print(synset)

        synsets.append(synset)

    return synsets

