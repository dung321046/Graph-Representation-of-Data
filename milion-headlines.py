import numpy as np
import pandas as pd
from tqdm import tqdm

data = pd.read_csv("./data/abcnews-date-text.csv")  # ["headline_text"]
data = data.sample(n=10, axis=0)
data = data.to_numpy()
import spacy

nlp = spacy.load("en_core_web_md")
names = []
edges_by_name = []
types = []
value_att = []
from co_occurrence.concept_manager import ConceptManager

cm = ConceptManager()
for datum in data:
    print(datum[1])
    tokens = nlp(datum[1])
    cm.update(tokens, datum[0])

from drawing.draw_graph import draw_graph

path = "./output/"
prefix = "abcnews-graph"
config = "simple"
FONT_SCALE = 5
cm.select_kw(path)
draw_graph(path, prefix, config, edges_by_name, names, types, value_att, FONT_SCALE)

# for i in tqdm(data.index):
#     print(data[i])
