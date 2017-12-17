from itertools import chain

from ds.implied_alignments import generate_implied_alignments, get_explicit_subtrees
from ds.nlg import generate_natural_language
from ds.sentence_tree import DynamicTree, SubTree


def generate_potential_extractions(sentence1, sentence2, alignments):
    subtree1, subtree2 = get_explicit_subtrees(sentence1, sentence2, alignments)
    outertree1 = create_outertree(sentence1, subtree1)
    outertree2 = create_outertree(sentence2, subtree2)

    dummy1 = SubTree([sentence1.root], [sentence1.root.children[0]])
    dummy2 = SubTree([sentence2.root], [sentence2.root.children[0]])
    fulltree1 = SubTree(sentence1.root.children[0].modifier.get_subtree_nodes(), [])
    fulltree2 = SubTree(sentence2.root.children[0].modifier.get_subtree_nodes(), [])

    alignments1 = {subtree1.root: (subtree1, fulltree2), fulltree2.root: (subtree1, fulltree2)}
    alignments2 = {subtree2.root: (fulltree1, subtree2), fulltree1.root: (fulltree1, subtree2)}

    extraction1 = generate_potential_entailments_local(outertree1, dummy2, sentence1, sentence2, None, alignments1)
    extraction2 = generate_potential_entailments_local(dummy1, outertree2, sentence1, sentence2, None, alignments2)

    return [extraction1] + [extraction2]


def create_outertree(sentence, subtree):
    temp_tree = DynamicTree(None, sentence.root)
    edge = temp_tree.find_parent_edge(subtree.root)

    edge.head.children.remove(edge)
    nodes = temp_tree.root.get_subtree_nodes()
    edge.head.children.append(edge)

    return SubTree(nodes, [edge])


def generate_potential_entailments(sentence1, sentence2, alignments):
    alignments = generate_implied_alignments(sentence1, sentence2, alignments)
    alignments = create_alignments_dictionary(alignments)

    potential_entailments1 = generate_potential_entailments_recursive(sentence1.root, sentence1, sentence2, alignments)
    potential_entailments2 = generate_potential_entailments_recursive(sentence2.root, sentence1, sentence2, alignments)

    alignments1 = set(map(lambda x: x[0], potential_entailments1))
    # alignments2 = set(map(lambda x: '?'.join(x[0].split('?')[::-1]), potential_entailments2))
    alignments2 = set(map(lambda x: x[0], potential_entailments2))
    if alignments1 != alignments2:
        raise Exception('BUG! Traversing different trees yields different alignments!')

    return potential_entailments1


def create_alignments_dictionary(alignments):
    alignment_dictionary = {}
    for alignment in alignments:
        subtree1, subtree2 = alignment
        for node in subtree1.root.get_subtree_nodes() + subtree2.root.get_subtree_nodes():
            alignment_dictionary[node] = alignment
    return alignment_dictionary


def generate_potential_entailments_recursive(node, sentence1, sentence2, alignments):
    if node not in alignments:
        return []

    subtree1, subtree2 = alignments[node]
    prerequisite = get_parent_alignment(subtree1, subtree2, sentence1, sentence2, alignments)
    if prerequisite is None and not (is_root(subtree1, sentence1) and is_root(subtree2, sentence2)):
        return []
    potential_entailments = [generate_potential_entailments_local(subtree1, subtree2, sentence1, sentence2, prerequisite, alignments)]

    for edge in get_edges_from_subtree_to_tree(subtree1, sentence1):
        potential_entailments.extend(generate_potential_entailments_recursive(edge.modifier, sentence1, sentence2, alignments))

    return potential_entailments


def get_parent_alignment(subtree1, subtree2, sentence1, sentence2, alignments):
    parent1 = sentence1.find_parent_edge(subtree1.root)
    parent2 = sentence2.find_parent_edge(subtree2.root)
    if parent1 is None or parent2 is None:
        return None

    parent1 = parent1.head
    parent2 = parent2.head
    if parent1 not in alignments or parent2 not in alignments:
        return None

    parent_alignment = alignments[parent1]
    if parent_alignment != alignments[parent2]:
        return None

    return parent_alignment


def is_root(subtree, tree):
    return subtree.root == tree.root


def generate_potential_entailments_local(subtree1, subtree2, sentence1, sentence2, prerequisite, alignments):
    entailment = generate_entailment_string(subtree1, subtree2)
    prerequisite = generate_entailment_string(*prerequisite) if prerequisite is not None else ''

    args1, template1 = generate_template(sentence1, subtree1, sentence2, subtree2, alignments)
    args2, template2 = generate_template(sentence2, subtree2, sentence1, subtree1, alignments)

    return entailment, prerequisite, generate_natural_language(sentence1, subtree1), generate_natural_language(sentence2, subtree2), args1, args2, template1, template2


def generate_entailment_string(subtree1, subtree2):
    nodes1 = sorted([node.id_.split(':')[1] for node in subtree1.root.get_subtree_nodes()])
    nodes2 = sorted([node.id_.split(':')[1] for node in subtree2.root.get_subtree_nodes()])
    return ' ? '.join((' '.join(nodes1), ' '.join(nodes2)))


def generate_template(hypothesis_tree, hypothesis_subtree, premise_tree, premise_subtree, alignments):
    hypothesis_tree = DynamicTree(None, hypothesis_tree.root)
    outgoing_edges = get_edges_from_subtree_to_tree(hypothesis_subtree, hypothesis_tree)
    aligned_edges = {edge: get_aligned_edge_id(edge, alignments) for edge in outgoing_edges}
    interesting_edges = [edge for edge in outgoing_edges if edge.is_slot() or aligned_edges[edge] is not None]

    # Generate the original arguments (children) of the hypothesis subtree
    args = [(edge.id_.split(':')[1], generate_natural_language(edge.modifier), aligned_edges[edge]) for edge in interesting_edges]

    # Replace hypothesis subtree's children with placeholders
    slot_i = 0
    for edge in outgoing_edges:
        if edge in interesting_edges:
            edge.modifier.children = []
            edge.modifier.word = 'SLOT' + str(slot_i) + '!'
            slot_i += 1
        else:
            edge.head.children.remove(edge)

    # Replace hypothesis subtree's parents with the (aligned) premise subtree's parents
    hypothesis_subtree_root = hypothesis_tree.find_node(hypothesis_subtree.root)
    if premise_tree.root == premise_subtree.root:
        premise_tree = DynamicTree(None, hypothesis_subtree_root)
    else:
        premise_tree = DynamicTree(None, premise_tree.root)
        premise_tree.find_parent_edge(premise_subtree.root).modifier = hypothesis_subtree_root

    # Generate the template
    template = generate_natural_language(premise_tree, hypothesis_subtree)

    return args, template


def get_edges_from_subtree_to_tree(subtree, tree):
    nodes = set(subtree.root.get_subtree_nodes())
    edges = list(chain(*[[edge for edge in tree.find_node(node).children if edge.modifier not in nodes] for node in nodes]))
    return sorted(edges, key=lambda e: int(e.id_.split(':')[1][:-1]))


def get_aligned_edge_id(edge, alignments):
    if edge.modifier not in alignments:
        return None
    subtree1, subtree2 = alignments[edge.modifier]
    if subtree1.root == edge.modifier and subtree2.root != edge.modifier:
        subtree = subtree2
    elif subtree1.root != edge.modifier and subtree2.root == edge.modifier:
        subtree = subtree1
    else:
        raise Exception('HORRIBLE BUG!!!    ' + str(edge.modifier) + '    ' + str(subtree1.root) + '    ' + str(subtree2.root))
    return subtree.root.id_.split(':')[1] + '*'
