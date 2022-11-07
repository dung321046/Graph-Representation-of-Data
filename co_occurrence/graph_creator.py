class GraphCreator:
    def __init__(self, form_dict, loc_dict):
        self.names = []
        self.types = []
        self.edges_by_name = []
        self.att_value = []
        for k, v in loc_dict.items():
            self.names.append(k)
            self.types.append(k[0])
            self.att_value.append(len(v))
        self.att_att_value = dict()
        n = len(self.names)
        for i in range(n):
            for j in range(n):
                if i != j:
                    self.att_att_value[(i, j)] = len(loc_dict[self.names[i]].intersection(loc_dict[self.names[j]]))
        sorted_dic = sorted(self.att_att_value.items(), key=lambda x: x[1], reverse=True)
        for t in sorted_dic[:40]:
            edge = (self.names[t[0][0]], self.names[t[0][1]])
            self.edges_by_name.append(edge)
        # print(sorted_dic)
