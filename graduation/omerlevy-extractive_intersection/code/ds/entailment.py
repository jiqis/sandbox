from collections import defaultdict
from itertools import chain
from ds.sentence_tree import SubTree


class Entailment:

    def __init__(self, id_, subtree1, edges1, subtree2, edges2, type_):
        self.id_ = id_
        self.subtree1 = subtree1
        self.edges1 = edges1
        self.subtree2 = subtree2
        self.edges2 = edges2
        self.type_ = type_

    def entailed(self):
        if self.type_ == '=':
            return [(self.subtree1, self.edges1), (self.subtree2, self.edges2)]
        elif self.type_ == '>':
            return [(self.subtree2, self.edges2)]
        else:
            return [(self.subtree1, self.edges1)]

    def __hash__(self):
        return hash(self.id_)

    def __eq__(self, other):
        return self.id_ == other.id_


def create_entailments_dictionary(sentence1, sentence2, entailments):
    edge_entailments = [zip(entailment.edges1, entailment.edges2) for entailment in entailments]
    edge_entailments = set(chain(*edge_entailments))

    modifier_entailments = set([(e1.modifier, e2.modifier) for e1, e2 in edge_entailments if e1.modifier is not None and e2.modifier is not None])
    parent_aligned_entailments = [entailment for entailment in entailments if (entailment.subtree1.root, entailment.subtree2.root) in modifier_entailments]
    root_entailments = [entailment for entailment in entailments if entailment.subtree1.root == sentence1.root or entailment.subtree2.root == sentence2.root]
    entailments = root_entailments + parent_aligned_entailments

    subtree_entailments = [(entailment.subtree1, entailment) for entailment in entailments] + [(entailment.subtree2, entailment) for entailment in entailments]
    subtree_entailments = [(element, entailment) for subtree, entailment in subtree_entailments for element in subtree.root.get_subtree_elements()]

    entailments = defaultdict(list)
    for element, entailment in subtree_entailments:
        entailments[element].extend(entailment.entailed())

    edge_entailments = dict(list(edge_entailments) + [(e2, e1) for e1, e2 in edge_entailments])

    return entailments, edge_entailments
