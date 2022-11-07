import numpy as np
import pandas as pd
from tqdm import tqdm

data = pd.read_csv("./data/abcnews-date-text.csv")  # ["headline_text"]
# For the fist method need to select data which share some of the nodes

data = data.sample(n=100, axis=0, random_state=0)
data = data.to_numpy()
import spacy

nlp = spacy.load("en_core_web_md")
from co_occurrence.concept_manager import ConceptManager

cm = ConceptManager()
for i, datum in enumerate(data):
    print(datum[1])
    tokens = nlp(datum[1])
    #print([nc.text for nc in tokens.noun_chunks])
    cm.update_noun_chunks(tokens, datum[0])

from drawing.draw_graph import draw_graph
import pickle

path = "./output/"
prefix = "abcnews-graph"
config = "simple"
FONT_SCALE = 20

cm.select_kw(path)

with open(path + "/form", "rb") as fp:
    form_dict = pickle.load(fp)
with open(path + "/loc", "rb") as fp:
    loc_dict = pickle.load(fp)

from co_occurrence.graph_creator import GraphCreator

graph_con = GraphCreator(form_dict, loc_dict)

draw_graph(path, prefix, config, graph_con.edges_by_name, graph_con.names, graph_con.types, graph_con.att_value,
           FONT_SCALE)

# for i in tqdm(data.index):
#     print(data[i])
