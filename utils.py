
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


order = []

def topological_sort(graph: dict):
    for n in graph.keys():
        n.reset()
    id = 0
    global order
    order = []
    for n in graph.keys():
        if not n.visit:
            if not valid_graph(graph, n, id):
                return False, None
            id += 1
    return True, order
    
def valid_graph(graph: dict, n: Node, id: int):
    n.visit = True
    n.id = id
    global order
    if all(map(lambda x: x.visit and x.id != id, graph[n])):
        order.insert(0, n.name + '.c')
        return True
    for u in graph[n]:
        u.pi = n
        if u.visit:
            if u.id == id:
                return False
        else:
            if not valid_graph(graph, u, id):
                return False
    order.insert(0, n.name + '.c')
    return True