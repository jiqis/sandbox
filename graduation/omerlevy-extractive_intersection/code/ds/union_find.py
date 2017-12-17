

class UnionFind:

    def __init__(self, x):
        self.x = x
        self.parent = self
        self.rank = 0

    def union(self, x):
        self_root = self.find()
        x_root = x.find()
        if x_root.rank > self_root.rank:
            self_root.parent = x_root
        elif x_root.rank < self_root.rank:
            x_root.parent = self_root
        elif x_root != self_root:
            self_root.parent = x_root
            x_root.rank += 1

    def find(self):
        if self.parent == self:
            return self
        else:
            self.parent = self.parent.find()
            return self.parent


def create_uf_dict(iterable):
    return {x: UnionFind(x) for x in iterable}


def create_partition(uf_dict):
    partition = {x: {x} for x in uf_dict.keys()}
    for x, uf_x in uf_dict.iteritems():
        partition[x] = partition[uf_x.find().x]
        partition[x].add(x)
    return partition