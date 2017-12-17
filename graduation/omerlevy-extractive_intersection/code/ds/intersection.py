from itertools import chain
from sentence_tree import DynamicTree


def intersection(sentence1, sentence2, entailments):
    intersections1 = intersection_node(sentence1.root, None, None, entailments)
    intersections2 = intersection_node(sentence2.root, None, None, entailments)

    if len(intersections1) != len(intersections2):
        raise Exception('BUG!!!!!!!!!!')

    return set(intersections1 + intersections2) #TODO check if they aren't equivalent. They should be


def intersection_node(node, tree, parent_edge, entailments):
    if node not in entailments:
        if tree is None:
            return []
        else:
            return [tree.add_placeholder(parent_edge)[0]]

    result_trees = []
    for subtree, edges in entailments[node]:
        if tree is None:
            new_tree = DynamicTree(None, subtree.root)
        else:
            new_tree = tree.add_subtree(subtree, parent_edge)

        temp_result_trees = [new_tree]
        for edge in edges:
            if edge is not None:
                tree_iterator = [intersection_node(edge.modifier, temp_tree, edge, entailments) for temp_tree in temp_result_trees]
                temp_result_trees = list(chain(*tree_iterator))
            else:
                temp_result_trees = []
        result_trees.extend(temp_result_trees)

    return result_trees

