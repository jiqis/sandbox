from itertools import chain
from ds.sentence_tree import Node, SubTree
from ds.sentences2alignment import partition
from ds.union_find import create_uf_dict, create_partition


def get_explicit_subtrees(sentence1, sentence2, alignments):
    alignments = [(sequence2nodes(seq1, sentence1, 's1:'), sequence2nodes(seq2, sentence2, 's2:')) for seq1, seq2 in alignments]
    nodes1, nodes2 = zip(*alignments)

    nodes1 = list(chain(*nodes1))
    nodes2 = list(chain(*nodes2))

    lca1 = lowest_common_ancestor(sentence1, get_roots(nodes1))
    lca2 = lowest_common_ancestor(sentence2, get_roots(nodes2))

    return SubTree(lca1.get_subtree_nodes(), []), SubTree(lca2.get_subtree_nodes(), [])


def generate_implied_alignments(sentence1, sentence2, alignments):
    uf = create_uf_dict(sentence1.root.get_subtree_nodes() + sentence2.root.get_subtree_nodes())

    add_glue_groups(uf, sentence1)
    add_glue_groups(uf, sentence2)

    add_explicit_alignments(uf, sentence1, sentence2, alignments)

    ad_nauseam(uf, sentence1, sentence2)

    return [(SubTree(nodes1, []), SubTree(nodes2, [])) for nodes1, nodes2 in create_alignments(uf)]


def add_explicit_alignments(uf, sentence1, sentence2, alignments):
    alignments = [(sequence2nodes(seq1, sentence1, 's1:'), sequence2nodes(seq2, sentence2, 's2:')) for seq1, seq2 in alignments]
    for nodes1, nodes2 in alignments:
        root = nodes1[0]
        for node in nodes1[1:] + nodes2:
            uf[root].union(uf[node])


def sequence2nodes(sequence, sentence, prefix):
    return [id2node(sentence, prefix + id_) for id_ in sequence]


def id2node(sentence, node_id):
    return sentence.find_node(Node(node_id, None, None))


def create_alignments(uf):
    alignments = []
    groups = set(map(frozenset, create_partition(uf).values()))
    for group in groups:
        nodes1 = [node for node in group if node.id_[:3] == 's1:']
        nodes2 = [node for node in group if node.id_[:3] == 's2:']
        if len(nodes1) >= 1 and len(nodes2) >= 1:
            alignments.append((nodes1, nodes2))
    return alignments


def add_glue_groups(uf, sentence):
    for node, group in partition(sentence):
        node = uf[id2node(sentence, node)]
        for neighbor in group:
            node.union(uf[id2node(sentence, neighbor)])


def ad_nauseam(uf, sentence1, sentence2):
    found_missing_alignments = True
    while found_missing_alignments:
        found_missing_nodes = True
        while found_missing_nodes:
            found_missing_nodes = add_intra_sentence_paths(uf, sentence1, sentence2)
        found_missing_alignments = add_inverse_inheritance(uf, sentence1, sentence2)


def add_intra_sentence_paths(uf, sentence1, sentence2):
    found_missing_nodes = False
    alignments = create_alignments(uf)

    for nodes1, nodes2 in alignments:
        missing_nodes1 = find_missing_intra_sentence_paths(sentence1, nodes1)
        for node in missing_nodes1:
            uf[nodes1[0]].union(uf[node])

        missing_nodes2 = find_missing_intra_sentence_paths(sentence2, nodes2)
        for node in missing_nodes2:
            uf[nodes2[0]].union(uf[node])

        if len(missing_nodes1 + missing_nodes2) > 0:
            found_missing_nodes = True

    return found_missing_nodes


def find_missing_intra_sentence_paths(sentence, nodes):
    roots = get_roots(nodes)
    if len(roots) == 1:
        return []

    lca = lowest_common_ancestor(sentence, roots)
    paths = [set(parent_child_path(sentence, lca, root)) for root in roots]
    connecting_nodes = set.union(*paths)
    return list(connecting_nodes.difference(nodes))


def get_roots(nodes):
    return [node for node in nodes if not any(any(edge.modifier == node for edge in other.children) for other in nodes)]


def lowest_common_ancestor(sentence, nodes):
    root = sentence.root
    paths = [parent_child_path(sentence, root, node) for node in nodes]
    shortest_path = sorted((len(path), path) for path in paths)[0][1]
    for i, ancestor in enumerate(shortest_path):
        if any(path[i] != ancestor for path in paths):
            return shortest_path[i-1]
    return shortest_path[-1]


def parent_child_path(sentence, parent, child):
    path = []
    node = child
    while node is not None and node != parent:
        path.insert(0, node)
        node = sentence.find_parent_edge(node).head
    if node is None:
        return None
    else:
        path.insert(0, node)
        return path


def add_inverse_inheritance(uf, sentence1, sentence2):
    found_missing_alignments = False
    alignments = create_alignments(uf)

    for nodes1, nodes2 in alignments:
        parent1 = get_parent(sentence1, nodes1)
        parent2 = get_parent(sentence2, nodes2)

        if uf[parent1].find() != uf[parent2].find():
            uf[parent1].union(uf[parent2])
            found_missing_alignments = True

    return found_missing_alignments


def get_parent(sentence, nodes):
    root = get_roots(nodes)[0]
    parent_edge = sentence.find_parent_edge(root)
    if parent_edge is None:
        return root
    return parent_edge.head
