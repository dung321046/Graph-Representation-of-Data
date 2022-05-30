import math
import networkx as nx
import random

VERB_TYPE = "v"
NOUN_TYPE = "n"
ROOT_TYPE = "r"

JP_Legend_dict = {
    "Root node": ROOT_TYPE,
    "Noun": NOUN_TYPE,
    "Verb": VERB_TYPE,
}
Color_types = {
    ROOT_TYPE: "#FFAA00",
    VERB_TYPE: "#E11E45",
    NOUN_TYPE: "#BA1EE1",
}


def get_node_size(value):
    return value


def get_color_dict(names, types):
    color_dict_by_name = dict()
    for idx, name in enumerate(names):
        color_dict_by_name[name] = Color_types[types[idx]]
    return color_dict_by_name


def adjust_order(freq):
    return min(50, freq) * 0.8 + min(max(0, freq - 50), 50) * 0.3 + max(0, freq - 100) * 0.1


def adjust_node_by_layers(pos, layers):
    for layer_id in range(len(layers)):
        layer = layers[layer_id]
        # if layer_id < 2:
        #     continue
        n = len(layer)
        for t in range(4):
            if t < 2:
                pos[layer[0]][0] = max(-math.pi, pos[layer[0]][0] - 0.2)
                pos[layer[n - 1]][0] = min(math.pi - 0.4, pos[layer[n - 1]][0] + 0.14)
            for i in range(1, n - 1):
                left = layer[i - 1]
                right = layer[i + 1]
                cur = layer[i]
                # if min(pos[cur][0] - pos[left][0], pos[right][0] - pos[cur][0]) > math.pi / 6.0:
                #     pos[left][0] = pos[left][0] + math.pi / 7.0
                #     pos[cur][0] = pos[cur][0] - math.pi / 7.0
                pos[cur][0] = (pos[left][0] + pos[right][0]) / 2
    for layer_id in range(len(layers)):
        if layer_id in [4, 5, 6, 7]:
            layer = layers[layer_id]
            n = len(layer)
            for t in range(20):
                if t < 2:
                    pos[layer[0]][0] = max(-math.pi, pos[layer[0]][0] - 0.2)
                    pos[layer[n - 1]][0] = min(math.pi - 0.4, pos[layer[n - 1]][0] + 0.1)
                for i in range(1, n - 1):
                    left = layer[i - 1]
                    right = layer[i + 1]
                    cur = layer[i]
                    # if min(pos[cur][0] - pos[left][0], pos[right][0] - pos[cur][0]) > math.pi / 6.0:
                    #     pos[left][0] = pos[left][0] + math.pi / 7.0
                    #     pos[cur][0] = pos[cur][0] - math.pi / 7.0
                    pos[cur][0] = (pos[left][0] + pos[right][0]) / 2


def hierarchy_pos_henry(G, root=None, width=1., vert_gap=0.2):
    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))
    visited = set()
    node_sizes = dict()
    _ratio = 0.5
    _single_width = 0.4

    def calculate_node_sizes(node):
        children = list(G.neighbors(node))
        visited.add(node)
        size = _single_width
        for child in children:
            if child not in visited:
                calculate_node_sizes(child)
                size += node_sizes[child] * _ratio
        node_sizes[node] = size
        return

    calculate_node_sizes(root)
    visited = set()
    vert_gap = 0.5
    pos = dict()
    layer_node = dict()
    SCALE = 1.1
    random.seed(27)
    parent_dict = dict()

    def calculate_pos(node, left, right, depth, is_left, is_right):
        delta = (right - left) * 0.2
        if depth < 3:
            center = (left + right) / 2
            pos[node] = [center, depth ** SCALE * vert_gap]
        elif (is_left and is_right) or (not is_left and not is_right):
            center = (left + right) / 2
            pos[node] = [center, depth ** SCALE * vert_gap]
        elif is_left:
            pos[node] = [left + delta, depth ** SCALE * vert_gap]
            # pos[node] = [left + delta, (depth ** 1.1 - 0.11) * vert_gap]
        elif is_right:
            pos[node] = [right - delta, depth ** SCALE * vert_gap]
            # pos[node] = [right - delta, (depth ** 1.1 + 0.05) * vert_gap]
        visited.add(node)
        if depth not in layer_node:
            layer_node[depth] = []
        layer_node[depth].append(node)
        children = list(G.neighbors(node))
        random.shuffle(children)
        cur_left = left
        # pre_center = left
        csizes = []
        sum_weight = 0
        for child in children:
            if child not in visited:
                csizes.append(node_sizes[child])
                sum_weight += node_sizes[child]
        i = 0
        is_used = 0
        for child in children:
            if child not in visited:
                # if node_sizes[child] < 0.
                parent_dict[child] = node
                cwidth = (right - left) * node_sizes[child] / sum_weight
                real_left = cur_left
                real_right = cur_left + cwidth
                if csizes[i] > _single_width:
                    if is_used > 0:
                        real_left = cur_left - _single_width * is_used / sum_weight
                        is_used = 0
                    if i < len(csizes) - 1 and csizes[i + 1] <= _single_width:
                        real_right = real_right + _single_width / sum_weight
                        is_used = -1
                else:
                    is_used += 1
                if i < len(csizes) - 1:
                    real_right -= 0.1 / sum_weight
                calculate_pos(child, real_left, real_right, depth + 1, i == 0, i == len(csizes) - 1)
                cur_left = cur_left + cwidth
                i += 1

    calculate_pos(root, -width / 2, width / 2, 0, False, False)
    adjust_node_by_layers(pos, layer_node)
    return pos
