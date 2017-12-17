from entailment import Entailment
from sentence_tree import DynamicTree, Edge, Node, SubTree


def read_file(path):
    with open(path) as fin:
        lines = [line.strip() for line in fin]

    splits = [i for i, line in enumerate(lines) if line == '']
    if len(splits) != 2:
        raise Exception('Wrong number of splits: ' + str(splits))
    
    sentence1 = parse_sentence(lines[:splits[0]], 's1:')
    sentence2 = parse_sentence(lines[splits[0]+1:splits[1]], 's2:')
    entailments = parse_entailments(lines[splits[1]+1:], sentence1, sentence2, 's1:', 's2:')
    return sentence1, sentence2, entailments


def parse_sentence(lines, prefix):
    input_nodes = [line.split('\t') for line in lines]
    nodes = {id_: Node(prefix + id_, word, []) for id_, word, parent, dependency in input_nodes}
    root = Node(prefix + '-1', '', [])
    nodes['-1'] = root
    for id_, word, parent, dependency in input_nodes:
        edge = Edge(prefix + id_ + '*', nodes[id_], nodes[parent], dependency)
        nodes[parent].children.append(edge)
    return DynamicTree(None, root)


def parse_entailments(lines, sentence1, sentence2, prefix1, prefix2):
    entailments = []
    for line in lines:
        for type_ in ('=', '>', '<', ''):
            if type_ == '':
                raise Exception('No separator: ' + str(line))
            if type_ in line:
                seq1, seq2 = line.split(type_)
                break
        subtree1, edges1 = parse_subsequence(seq1, sentence1, prefix1)
        subtree2, edges2 = parse_subsequence(seq2, sentence2, prefix2)
        entailments.append(Entailment(line, subtree1, edges1, subtree2, edges2, type_))
    return entailments


def parse_subsequence(seq, sentence, prefix):
    if ':' in seq:
        tokens = seq.split(':')
        edges = [parse_edge(edge, sentence, prefix) for edge in tokens[1].split()]
        seq = tokens[0]
    else:
        edges = []

    tokens = seq.split()
    nodes = [sentence.find_node(Node(prefix + id_, None, None)) for id_ in tokens]
    subtree = SubTree(nodes, edges)

    return subtree, edges


def parse_edge(edge, sentence, prefix):
    if edge[0] == '*':
        return Edge(prefix + edge, None, None, None)
    else:
        return sentence.find_edge(Edge(prefix + edge, None, None, None))
