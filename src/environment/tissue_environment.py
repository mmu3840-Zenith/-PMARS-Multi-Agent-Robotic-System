import networkx as nx
import random

class TissueEnvironment:
    def __init__(self, n=10):
        self.graph = nx.erdos_renyi_graph(n, 0.3)
        self.failed = set()

    def inject_failure(self, node):
        self.failed.add(node)

    def propagate(self):
        new_failures = set()
        for node in self.failed:
            for n in self.graph.neighbors(node):
                if random.random() < 0.2:
                    new_failures.add(n)
        self.failed.update(new_failures)
