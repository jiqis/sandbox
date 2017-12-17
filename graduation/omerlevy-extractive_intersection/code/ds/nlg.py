from itertools import chain

from ds.sentence_tree import DynamicTree, Edge, SubTree


def generate_natural_language(root, bold_subtree=None, edge_entailments=None):
    if edge_entailments is not None:
        root = clean_placeholders(root, edge_entailments)

    if isinstance(root, DynamicTree) or isinstance(root, SubTree):
        root = root.root
    nodes = generate_natural_language_recursive(root)

    if bold_subtree is not None:
        bold = set([node.id_ for node in bold_subtree.root.get_subtree_nodes()])
    else:
        bold = set()
    nodes = ['<span class="emph">' + node.word + '</span>' if node.id_ in bold else node.word for node in nodes]

    return ' '.join(nodes).strip()


def generate_natural_language_recursive(root):
    nodes = sorted([(id2int(root.id_), [root])] +
                   [(id2int(edge.id_), generate_natural_language_recursive(edge.modifier)) for edge in root.children])
    return list(chain(*zip(*nodes)[1]))


def id2int(id_):
    n = id_.split(':')[1]
    if n[-1] == '*':
        n = n[:-1]
    return int(n)


def clean_placeholders(sentence, edge_entailments):
    sentence = DynamicTree(None, sentence.root)

    nodes = sentence.root.get_subtree_nodes()
    nonslots = [node for node in nodes if node.word == '[some*]' and not sentence.find_parent_edge(node).is_slot()]
    for node in nonslots:
        edge = sentence.find_parent_edge(node)
        edge.head.children.remove(edge)

    nodes = sentence.root.get_subtree_nodes()
    slots = [node for node in nodes if node.word == '[some*]']
    for node in slots:
        edge = Edge(node.id_ + '*', None, None, None)
        if edge in edge_entailments:
            edge_id = edge_entailments[edge].id_.split(':')[1]
            if edge_id[0] == '*':
                node.word = node.word.replace('*', edge_id[1:])

    return sentence