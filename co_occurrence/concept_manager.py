import pickle
from drawing.nx_utils import VERB_TYPE, NOUN_TYPE


def get_concept(word, type):
    ans = word
    if type == "VERB":
        ans = VERB_TYPE + ans
    else:
        ans = NOUN_TYPE + ans
    return ans


class ConceptManager:
    def __init__(self):
        self.loc_dict = dict()
        self.form_dict = dict()

    def update_noun_chunks(self, tokens, index):
        for nc in tokens.noun_chunks:
            word = nc.text
            # print(word)
            concept = NOUN_TYPE + word
            if concept not in self.loc_dict:
                self.loc_dict[concept] = {index}
                self.form_dict[concept] = {word}
            else:
                self.loc_dict[concept].add(index)
                self.form_dict[concept].add(word)

    def update(self, tokens, index):
        start = 0
        end = 0
        n = len(tokens)
        while start < n - 1:
            while end < n - 1:
                if tokens[start].pos_ == tokens[end + 1].pos_:
                    end += 1
                    continue
                break
            word = " ".join([t.text for t in tokens[start:end + 1]])
            # print(word)
            concept = get_concept(word, tokens[start].pos_)
            if concept not in self.loc_dict:
                self.loc_dict[concept] = {index}
                self.form_dict[concept] = {word}
            else:
                self.loc_dict[concept].add(index)
                self.form_dict[concept].add(word)
            start = end + 1
            end = start

    def select_kw(self, prefix):
        sorted_dic = sorted(self.loc_dict.items(), key=lambda x: len(x[1]), reverse=True)
        selected_attributes = [t[0] for t in sorted_dic]
        candidate_dict = dict()
        selected_loc_dict = dict()
        for att in selected_attributes:
            candidate_dict[att] = self.form_dict[att]
            selected_loc_dict[att] = self.loc_dict[att]

        with open(prefix + "/form", "wb") as fp:
            pickle.dump(candidate_dict, fp)
        with open(prefix + "/loc", "wb") as fp:
            pickle.dump(selected_loc_dict, fp)
