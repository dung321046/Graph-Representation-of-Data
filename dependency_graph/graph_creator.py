from drawing.nx_utils import VERB_TYPE, NOUN_TYPE


class GraphCreatorDirect:
    def __init__(self):
        self.names = []
        self.types = []
        self.name_idx = dict()
        self.edges_by_name = []
        self.att_value = []

    def add_concept(self, name):
        if name in self.name_idx:
            self.att_value[self.name_idx[name]] += 1
            return
        idx = len(self.names)
        self.name_idx[name] = idx
        self.names.append(name)
        self.types.append(NOUN_TYPE)
        self.att_value.append(1)

    def update(self, pairs):
        for pair in pairs:
            if pair[0] == pair[1]:
                continue
            self.add_concept(pair[0])
            self.add_concept(pair[1])
            self.edges_by_name.append(pair)

    def update_type(self, name, type):
        self.types[self.name_idx[name]] = type
