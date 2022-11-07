import numpy as np
import pandas as pd
from tqdm import tqdm
import spacy
from drawing.nx_utils import ROOT_TYPE
nlp = spacy.load("en_core_web_md")
data = pd.read_csv("./data/abcnews-date-text.csv")  # ["headline_text"]
# For the fist method need to select data which share some of the nodes

data = data.sample(n=100, axis=0, random_state=0)
data = data.to_numpy()
from dependency_graph import graph_creator
graph_con  = graph_creator.GraphCreatorDirect()
for datum in data:
    if "police" in datum[1]:
        print(datum[1])
        doc = nlp(datum[1])
        pairs = []
        for token in doc:
            print(token.text, token.dep_, token.head.text, [child for child in token.children])
            pairs.append((token.text, token.head.text))
        graph_con.update(pairs)
graph_con.update_type("police", ROOT_TYPE)
from drawing.draw_graph import draw_graph

path = "./output/"
prefix = "abcnews-graph"
config = "dependency"
FONT_SCALE = 40
draw_graph(path, prefix, config, graph_con.edges_by_name, graph_con.names, graph_con.types, graph_con.att_value,
           FONT_SCALE)
