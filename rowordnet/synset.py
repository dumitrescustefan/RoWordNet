from enum import Enum
from .exceptions import SynsetError


class Synset(object):

    class Pos(Enum):
        NOUN = 0
        VERB = 1
        ADVERB = 2
        ADJECTIVE = 3

        def __str__(self):
            dic_pos2chr = {'NOUN': 'n', 'VERB': 'v', 'ADVERB': 'r', 'ADJECTIVE': 'a'}
            return dic_pos2chr[self.name]

        def __repr__(self):
            return self.name

    class SumoType(Enum):
        HYPERNYM = 0
        EQUIVALENT = 1
        INSTANCE = 2
        BRACKET = 3
        POINTS = 4

        def __str__(self):
            dic_stp2chr = {'HYPERNYM': '+', 'EQUIVALENT': '=', 'INSTANCE': '@', 'BRACKET': '[', 'POINTS': ':'}
            return dic_stp2chr[self.name]

        def __repr__(self):
            return self.name

    def __init__(self, id: str, pos=None, nonlexicalized=None, definition=None, stamp=None, sentiwn=None, domain=None,
                 sumo=None, sumotype=None, literals=None, literals_senses=None):
        """
            Initialize a synset object:

            Args:
                id (str): The id of the synset.
                pos (Pos, optional): The pos of the synset.
                nonlexicalized (str): ?
                definition (str, optional): The definition of synset.
                stamp (str, optional): The stamp of the synset.
                sentiwn (list of ints/floats, optional): The sentiwn of the synset.
                domain (str, optional): The domain of the synset.
                sumo (str, optional): The sumo of the synset.
                sumotype (SumoType, optional): The type of sumo.
                literals (dict, optional): The literals of synsets. First argument represents the literal and the second
                    one represents the sense.

            Raises:
                TypeError: If any argument has incorrect type.

        """

        if not isinstance(id, str):
            raise TypeError("Argument 'id' has incorrect type, expected str, got {}".format(type(id).__name__))

        self._id = id
        self._literals = [] if literals is None else literals
        self._literals_senses = [] if literals_senses is None else literals_senses
        self._pos = pos
        self._definition = definition
        self._stamp = stamp
        self._domain = domain
        self._sumo = sumo
        self._sumotype = sumotype
        self._sentiwn = sentiwn
        self._nonlexicalized = nonlexicalized

    @property
    def id(self):
        """
            Get/set the id(str) of this synset.
            Getter returns the id.
            Setter recieves a string containing the id.
        """
        return self._id

    @property
    def literals(self):
        """
            Get/set the literals of this synset.
            Getter returns the literals of this synset.
            Setters recieves the literals as list.
        """
        return self._literals
        
    @literals.setter
    def literals(self, value: list):
        if not isinstance(value, list):
            raise TypeError("Argument 'value' has incorrect type, expected list, got {}".format(type(value).__name__))

        for literal in value:
            if not isinstance(literal, str):
                raise TypeError("Argument 'literal-value' has incorrect type, expected str, got {}"
                                .format(type(literal).__name__))

        self._literals_senses = ["" for i in range(len(value))]
        self._literals = value

    @property
    def literals_senses(self):
        """
            Get/set the senses for each literal of this synset. Senses's indexes correspond to literals's.
            Setter returns the senses of each literal of this synset.
            Setters recieves the senses as list.
        """

        return self._literals_senses

    @literals_senses.setter
    def literals_senses(self, value: list):
        if not isinstance(value, list):
            raise TypeError("Argument 'value' has incorrect type, expected list, got {}".format(type(value).__name__))

        for sense in value:
            if not isinstance(sense, str):
                raise TypeError("Argument 'sense-value' has incorrect type, expected str, got {}"
                                .format(type(sense).__name__))

        self._literals_senses = value
           
    @property
    def sentiwn(self):
        """
            Get/set the values for the SentiWordNet(list of floats/ints) of this synset.
            Getter returns a list of 3 values for Positive, Negative, Objective.
            Setter receives a list of 3 floats/ints to set the PNO values.
        """
        return self._sentiwn
        
    @sentiwn.setter
    def sentiwn(self, value: list):
        if not isinstance(value, list):
            raise TypeError("Argument 'value' has incorrect type, expected list, got {}".format(type(value).__name__))
        if not len(value) == 3:
            raise ValueError("Argument 'value' expected a list of size 3, but got a list of size {} instead"
                             .format(len(value)))
        if not all((isinstance(element, float) or (isinstance(element, int))
                    for element in value)):
            raise ValueError("Argument's 'value' values must be of type float/int")
        if not all(0 <= element <= 1 for element in value):
            raise ValueError("Argument's 'value' values must have values between 0 and 1")
        if not sum(value) == 1:
            raise ValueError("Argument's 'value' values must add up to 1")

        self._sentiwn = value

    @property
    def definition(self):
        """
            Get/set the definition(str) of this synset.
            Getter returns the definition of this synset.
            Setter receives a string containing the definition.
        """

        return self._definition

    @definition.setter
    def definition(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Argument 'value' has incorrect type, expected str, got {}".format(type(value).__name__))

        self._definition = value

    @property
    def pos(self):
        """
            Get/set the pos(Pos) of this synset.
            Getter returns the pos of this synset.
            Setter receives the pos value of this synset.
        """
        return self._pos

    @pos.setter
    def pos(self, value: Pos):
        if not isinstance(value, self.Pos):
            raise TypeError("Argument 'value' has incorrect type, expected str, got {}".format(type(value).__name__))
        self._pos = value

    @property
    def domain(self):
        """
            Gets/sets the domain of this synset.
            Getter returns the domain of this synset.
            Setter receives a string containing the domain.
        """

        return self._domain

    @domain.setter
    def domain(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Argument 'value' has incorrect type, expected str, got {}".format(type(value).__name__))

        self._domain = value

    @property
    def sumo(self):
        """
            Gets/sets the sumo of this synset.
            Getter returns the sumo of this synset.
            Setter receives a string containing the sumo.
        """

        return self._sumo

    @sumo.setter
    def sumo(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Argument 'value' has incorrect type, expected str, got {}".format(type(value).__name__))

        self._sumo = value

    @property
    def sumotype(self):
        """
            Gets/sets the sumotype(HYPERNYM, EQUIVALENT, INSTANCE) of this synset.
            Getter returns the sumotype of this synset.
            Setter receives a synset SumoType(HYPERNYM, EQUIVALENT, INSTANCE)
        """

        return self._sumotype

    @sumotype.setter
    def sumotype(self, value: SumoType):
        if not isinstance(value, self.SumoType):
            raise TypeError("Argument 'value' has incorrect type, expected SumoType, got {}"
                            .format(type(value).__name__))

        self._sumotype = value

    @property
    def nonlexicalized(self):
        """
            Gets/sets the nonlexicalized attribute of this synset.
            Getter returns the nonlexicalized attribute
            Setter recieves a string containing the nonlexicalized value.
        """

        return self._nonlexicalized

    @nonlexicalized.setter
    def nonlexicalized(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Argument 'value' has incorrect type, expected bool, got {}".format(type(value).__name__))

        self._nonlexicalized = value

    @property
    def stamp(self):
        """
            Gets/sets the stamp of this synset.
            Getter returns the stamp of this synset.
            Setter recieves a string containing the stamp or None.
        """

        return self._stamp

    @stamp.setter
    def stamp(self, value: str):
        if not isinstance(value, str) and value is not None:
            raise TypeError("Argument 'value' has incorrect type, expected str, got {}".format(type(value).__name__))

        self._stamp = value

    def add_literal(self, literal: str, sense: str=""):
        """
            Add a literal to the synset.

            Args:
                literal (str): The value of the literal.
                sense (str): Sense of the literal.

            Raises:
                SynsetError: If the literal is already in the synset.
        """
        if literal in self._literals:
            raise SynsetError("Literal '{}' is already in the synset".format(literal))

        self._literals.append(literal)
        self._literals_senses.append(sense)

    def remove_literal(self, literal: str):
        """
            Remove a literal from the synset.

            Args:
                literal (str): Literal of the synset.

            Raises:
                SynsetError: If there's no literal with this value in the synset.
        """

        if literal not in self._literals:
            raise SynsetError("literal '{}' is not in the synset".format(literal))

        index = self._literals.index(literal)
        self._literals.remove(literal)
        del self._literals_senses[index]

    def __repr__(self):
        return "Synset(id={!r}, literals={!r}, definition={!r})".format(self._id, self._literals, self._definition)

    def __eq__(self, other):
        if isinstance(other, Synset):
            if (self.id == other.id and
                    self.literals == other.literals and
                    self.literals_senses == other.literals_senses and
                    self.pos == other.pos and
                    self.definition == other.definition and
                    self.stamp == other.stamp and
                    self.domain == other.domain and
                    self.sumo == other.sumo and
                    self.sumotype == other.sumotype and
                    self.sentiwn == other.sentiwn and
                    self.nonlexicalized == other.nonlexicalized):

                return True

        return False