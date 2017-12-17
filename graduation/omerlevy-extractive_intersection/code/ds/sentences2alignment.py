from ds.sentence_tree import Edge, Node
from ds.union_find import create_uf_dict, create_partition


def generate_groups(sentence1, sentence2):
    return dict(partition(sentence1) + partition(sentence2))


def partition(sentence):
    node_ids = [element.id_ for element in sentence.root.get_subtree_elements() if isinstance(element, Node)]
    ufs = create_uf_dict(node_ids)
    edges = [element for element in sentence.root.get_subtree_elements() if isinstance(element, Edge)]
    for edge in edges:
        if edge.is_glue():
            h, m = edge.head.id_, edge.modifier.id_
            ufs[h].union(ufs[m])

    groups = create_partition(ufs)
    return [(k, list(v)) for k, v in groups.iteritems()]
