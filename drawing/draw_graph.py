import matplotlib.pyplot as plt
from drawing.nx_utils import get_color_dict, adjust_order, hierarchy_pos_henry, JP_Legend_dict, ROOT_TYPE, \
    Color_types, get_node_size

import networkx as nx
import math


def draw_graph(path, prefix, config, edges_by_name, names, types, value_att, FONT_SCALE):
    G = nx.DiGraph()
    G.add_edges_from(edges_by_name)

    color_dict_by_name = get_color_dict(names, types)
    values = [color_dict_by_name[node] for node in G.nodes()]
    freq_dict_by_name = dict()
    order_dict_by_name = dict()
    for idx, name in enumerate(names):
        freq_dict_by_name[name] = adjust_order(value_att[idx])
        order_dict_by_name[name] = idx
    node_ratio = 10000 / max(list(freq_dict_by_name.values()))
    node_sizes = [get_node_size(freq_dict_by_name[node] * node_ratio) for node in G.nodes()]
    nodes = [node for node in G.nodes]
    if len(nodes) == 0:
        return
    root_id = 0
    for id, node in enumerate(nodes):
        if node == names[0]:
            root_id = id
            break
    pos = hierarchy_pos_henry(G, nodes[root_id], width=2 * math.pi, vert_gap=0.4)
    pos = {u: (r * math.cos(theta), r * math.sin(theta)) for u, (theta, r) in pos.items()}
    font_size = 5
    dpi = 1000
    arrowsize = 0.5
    nx.draw_networkx_edges(G, pos, edgelist=edges_by_name, arrows=False, arrowsize=arrowsize, alpha=0.2)
    nx.draw_networkx_nodes(G, pos, node_color=values, node_size=node_sizes, alpha=0.4)
    from matplotlib.pyplot import text
    max_font = min(1000 / math.log(len(nodes), 1.03), 30)
    font_ratio = max_font / math.log(max(value_att), FONT_SCALE)
    for node, (x, y) in pos.items():
        font_size = max(math.log(freq_dict_by_name[node] + 0.001, FONT_SCALE) * font_ratio, 5)
        text(x, y, node, fontsize=font_size, ha='center', va='center')

    f = plt.figure(1)
    ax = f.add_subplot(1, 1, 1)
    r = list(pos.values())[0]
    for label, type in JP_Legend_dict.items():
        ax.plot([r[0]], [r[1]], color=Color_types[type], alpha=0.4, marker='o', label=label)
    ax.plot([r[0]], [r[1]], color=Color_types[ROOT_TYPE], marker='o')
    plt.axis('off')
    f.set_facecolor('w')
    plt.legend(prop={'size': font_size})
    f.tight_layout()
    plt.savefig(path + "/" + prefix + "-" + config, dpi=dpi)
    plt.close()
