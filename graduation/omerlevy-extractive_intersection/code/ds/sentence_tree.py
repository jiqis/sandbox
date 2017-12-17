from ds.dependency_constants import GLUE_DEPENDENCIES, SLOT_DEPENDENCIES


class DynamicTree:
    '''
    Immutable.
    '''

    def __init__(self, id_, node=None):
        if node is None:
            self.root = Node(id_, '', [])
        else:
            self.root = node.copy()

    def add_subtree(self, subtree, parent_edge):
        if not isinstance(parent_edge, Edge):
            raise Exception('Expected parent to be Edge, but parent is ' + str(parent_edge))

        new_tree = DynamicTree(None, self.root)
        edge = new_tree.find_edge(parent_edge)
        if edge is None:
            raise Exception('Current edge not in tree!')

        new_node = subtree.root.copy()
        edge.modifier = new_node
        return new_tree

    def add_node(self, node, parent_edge):
        if not isinstance(parent_edge, Edge):
            raise Exception('Expected current to be Edge, but current is ' + str(parent_edge))

        new_tree = DynamicTree(None, self.root)
        edge = new_tree.find_edge(parent_edge)
        if edge is None:
            raise Exception('Current edge not in tree!')

        new_node = node.copy()
        edge.modifier = new_node
        return new_tree, new_node

    def add_placeholder(self, current):
        return self.add_node(Node(current.id_[:-1], '[some*]', []), current)

    def find_node(self, node):
        return self.find_node_recursive(self.root, node)

    def find_node_recursive(self, root, node):
        if root == node:
            return root
        for edge in root.children:
            result = self.find_node_recursive(edge.modifier, node)
            if result is not None:
                return result
        return None

    def find_edge(self, edge):
        return self.find_edge_recursive(self.root, edge)

    def find_edge_recursive(self, root, edge):
        if root is not None:
            for child in root.children:
                if child == edge:
                    return child
                result = self.find_edge_recursive(child.modifier, edge)
                if result is not None:
                    return result
        return None

    def find_parent_edge(self, node):
        if node == self.root:
            return None
        return self.find_parent_edge_recursive(self.root, node)

    def find_parent_edge_recursive(self, root, node):
        if root is not None:
            for child in root.children:
                if child.modifier == node:
                    return child
                result = self.find_parent_edge_recursive(child.modifier, node)
                if result is not None:
                    return result
        return None

    def __str__(self):
        return self.str_recursion(self.root)

    def str_recursion(self, root):
        s = root.word
        if len(root.children) > 0:
            s += '(' + ';'.join((child.dependency + '_' + self.str_recursion(child.modifier) for child in root.children)) + ')'
        return s

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)


class Node:

    def __init__(self, id_, word, children):
        self.id_ = id_
        self.word = word
        self.children = children

    def copy(self):
        node = Node(self.id_, self.word, None)
        node.children = [edge.copy(node) for edge in self.children]
        return node

    def get_subtree_elements(self):
        elements = [self] + self.children
        for child in self.children:
            if child.modifier is not None:
                elements.extend(child.modifier.get_subtree_elements())
        return elements

    def get_subtree_nodes(self):
        return filter(lambda x: isinstance(x, Node), self.get_subtree_elements())

    def __hash__(self):
        return hash(self.id_)

    def __eq__(self, other):
        return str(self.id_) == str(other.id_)

    def __str__(self):
        return str(self.id_) + ':' + self.word

    def __repr__(self):
        return str(self)


class Edge:

    def __init__(self, id_, modifier, head, dependency):
        self.id_ = id_
        self.modifier = modifier
        self.head = head
        self.dependency = dependency

    def copy(self, head):
        if self.modifier is None:
            return Edge(self.id_, None, head, self.dependency)
        else:
            return Edge(self.id_, self.modifier.copy(), head, self.dependency)

    def is_slot(self):
        return self.dependency in SLOT_DEPENDENCIES

    def is_glue(self):
        return self.dependency in GLUE_DEPENDENCIES

    def __hash__(self):
        return hash(self.id_)

    def __eq__(self, other):
        return str(self.id_) == str(other.id_)

    def __str__(self):
        return str(self.id_) + ':' + str(self.dependency)

    def __repr__(self):
        return str(self)


class SubTree:

    def __init__(self, nodes, outgoing_edges):
        self.root = self.get_root(nodes).copy()
        self.isolate_subtree(self.root, set(nodes), set(outgoing_edges))

    @staticmethod
    def get_root(nodes):
        roots = [node for node in nodes if not any(any(edge.modifier == node for edge in other.children) for other in nodes)]
        if len(roots) != 1:
            raise Exception('Number of roots: ' + str(len(roots)))
        return roots[0]

    def isolate_subtree(self, root, nodes, outgoing_edges):
        internal_edges = []
        for edge in root.children:
            if edge.modifier in nodes:
                internal_edges.append(edge)
                self.isolate_subtree(edge.modifier, nodes, outgoing_edges)
            elif edge in outgoing_edges:
                internal_edges.append(Edge(edge.id_, None, root, edge.dependency))
        root.children = internal_edges

