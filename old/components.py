from enum import Enum


class Literal(object):
    def __init__(self, literal=None, sense=None):
        self.literal = literal
        self.sense = sense

    def __repr__(self):
        return 'Literal(literal={!r}, sense={!r})'.format(self.literal, self.sense)


class Relation(object):
    def __init__(self, source_synet=None, target_synet=None, relation=None,
                 source_literal=None, target_literal=None):
        self.source_synet = source_synet
        self.target_synet = target_synet
        self.relation = relation
        self.source_literal = source_literal
        self.target_literal = target_literal

    def __repr__(self):
        return 'Relation(source_synet={!r}, relation={!r}, target_source={!r})'\
                .format(self.source_synet, self.relation, self.target_synet)


class Synset(object):
    Type = Enum('Type', 'NOUN VERB ADJECTIVE ADVERB')
    SumoType = Enum('SumoType', 'PLUS EQUAL AT BRACKET POINTS')

    def __init__(self, id=None, pos=None, nonlexicalized=None, definition=None,
                 stamp=None, domain=None, sumo=None, sumotype=None,
                 sentiwn_p=None, sentiwn_n=None, sentiwn_o=None, nl=None,
                 information_content=None,
                 pwn20=None, literals=None, usage=None, relations=None):
        
        self.pwn20 = [] if pwn20 is None else pwn20
        self.literals = [] if literals is None else literals
        self.usage = [] if usage is None else usage
        self.relations = [] if relations is None else relations
        self.id = id
        self.pos = pos
        self.nonlexicalized = nonlexicalized
        self.definition = definition
        self.stamp = stamp
        self.domain = domain
        self.sumo = sumo
        self.sumotype = sumotype
        self.sentiwn_p = sentiwn_p
        self.sentiwn_n = sentiwn_n
        self.sentiwn_o = sentiwn_o
        self.nl = nl
        self.information_content = information_content

    @classmethod
    def str_to_pos(cls, pos):
        if pos == 'n':
            return cls.Type.NOUN
        if pos == 'v':
            return cls.Type.VERB
        if pos == 'r':
            return cls.Type.ADVERB
        if pos == 'a':
            return cls.Type.ADJECTIVE

    @classmethod
    def str_to_sumo(cls, sumo):
        if sumo == '+':
            return cls.SumoType.PLUS
        if sumo == '=':
            return cls.SumoType.EQUAL
        if sumo == '@':
            return cls.SumoType.AT
        if sumo == '[':
            return cls.SumoType.BRACKET
        if sumo == ':':
            return cls.SumoType.POINTS

    def __repr__(self):
        output = 'Synset(id={!r}, pos={!r}, nl={!r}, stamp={!r}, domain={!r}\n\t  definition={!r}' \
                 '\n\t  Sumo={!r}, SumoType={!r}' \
                 '\n\t  sentiwn_p={!r}, sentiwn_n={!r}, sentiwn_o={!r}'.\
                 format(self.id, self.pos, self.nl, self.stamp, self.domain, self.definition,
                        self.sumo, self.sumotype, self.sentiwn_p, self.sentiwn_n, self.sentiwn_o)

        for literal in self.literals:
            output += '\n\t  {!r}'.format(literal)

        for relation in self.relations:
            output += '\n\t  {!r}'.format(relation)

        return output

