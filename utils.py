
class Node():

    def __init__(self, name):
        self.name = name
        self.visit = False
        self.pi = None
        self.id = 0
    
    def reset(self):
        self.visit = False
        self.pi = None

    def __repr__(self):
        return self.name



def dfs(graph: dict, n: Node):

    def dfs_rec(graph: dict, v: Node):
        v.visit = True
        for u in graph[v]:
            if not u.visit:
                dfs_rec(graph, u)

    for node in graph.keys():
        node.reset()
    
    dfs_rec(graph, n)
