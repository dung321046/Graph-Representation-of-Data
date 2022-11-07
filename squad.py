import json
import spacy
from drawing.nx_utils import ROOT_TYPE

nlp = spacy.load("en_core_web_md")
from dependency_graph import graph_creator

graph_con = graph_creator.GraphCreatorDirect()
with open("./data/squad/train-v2.0.json", "r") as f:
    data = json.load(f)
    print(data["data"][0])
    para = data["data"][0]["paragraphs"]
    pairs = []
    for p in para[:1]:
        # print(p["context"])
        doc = nlp(p["context"])
        sentences = [i for i in nlp(doc).sents]
        for sen in sentences:
            print(sen)
            for token in sen:
                # print(token.text, token.dep_, token.head.text, [child for child in token.children])
                pairs.append((token.text, token.head.text))
    graph_con.update(pairs)
from drawing.draw_graph import draw_graph

path = "./output/"
prefix = "squad-graph"
config = "dependency"
FONT_SCALE = 40
draw_graph(path, prefix, config, graph_con.edges_by_name, graph_con.names, graph_con.types, graph_con.att_value,
           FONT_SCALE)
