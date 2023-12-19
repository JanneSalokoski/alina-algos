""" graph-coloring.py - Distribute by coloring graph nodes"""

import applications

from time import perf_counter

import networkx as nx
import matplotlib.pyplot as plt

class Node:
    """Implement node for graph"""
    def __init__(self, name, color_options) -> None:
        self.name = name
        self.color_options = color_options

        self.neighbours = []
        self.color = None

class Graph:
    """Implement a general graph"""
    def __init__(self) -> None:
        self.nodes = {}

    def add_node(self, application):
        """Add a node to the graph"""
        self.nodes[application.id] = Node(application.id, application.requested_slots)

    def add_edge(self, node1, node2):
        """Add edge between `node1` and `node2`"""
        self.nodes[node1.name].neighbours.append(node2.name)

    def visit(self, node):
        if node in self.visited:
            return

        print(f"visit node: {node}")
        self.visited.add(node)

        for next in self.nodes[node].neighbours:
            self.visit(next)

    def dfs(self, start):
        self.visited = set()
        self.visit(start)

    def color_node(self, node):
        if node in self.visited:
            return

        self.visited.add(node)

        for color in self.nodes[node].color_options:
            if color not in self.used_colors:
                self.nodes[node].color = color
                self.used_colors.add(color)

                for next in self.nodes[node].neighbours:
                    self.color_node(next)

    def color(self, start):
        self.used_colors = set()
        self.visited = set()
        self.color_node(start)

def graph_coloring(slotspace: applications.SlotSpace,
    appls: list[applications.Application]) -> int:
    """Distribute slots by coloring graph nodes"""

    print(f"Slotspace: {slotspace}")
    print(f"Applications: {len(appls)}")

    print("Start distributing slots")
    t1 = perf_counter()

    graph = Graph()

    for appl in appls:
        graph.add_node(appl)

    print("Created nodes for applications")

    requests = {}
    for appl in appls:
        for slot in appl.requested_slots:
            if slot not in requests:
                requests[slot] = []

            requests[slot].append(appl.id)

    print("Created a dictionary of requests")

    for slot in requests:
        for id in requests[slot]:
            for id2 in requests[slot]:
                if id != id2:
                    graph.add_edge(graph.nodes[id], graph.nodes[id2])

    print("Created edges for nodes")

    graph.color(list(graph.nodes)[0])
    print("Colored nodes")

    for appl in appls:
        appl.reserve(graph.nodes[appl.id].color)

    t2 = perf_counter()
    print(f"Finished distributing slots in {t2-t1:.4f}s")

    df = applications.generate_dataframe(appls)
    df = df.sort_values(by=["reserved"])
    print(f"\nReserved slots:\n{df}\n")

    counts = df["reserved"].value_counts(dropna=False)

    none_amount = 0
    try:
        none_amount = counts[None]
    except Exception:
        print(f"All applications have a reserved slot!")

    percent = none_amount / len(appls)

    print(f"Applications without a reserved slot: {none_amount} -> {percent*100:.2f}%")

    #G = nx.Graph()

    #for appl in appls:
    #    G.add_node(appl.id)

    #for slot in requests:
    #    for id in requests[slot]:
    #        for id2 in requests[slot]:
    #            if id != id2:
    #                G.add_edge(graph.nodes[id].name, graph.nodes[id2].name)

    #nx.draw_circular(G, with_labels=True)

    #plt.savefig("graph.svg")

    return int(none_amount)

def main():
    """Run `prefer_sparse` with some data"""

    slotspace = applications.SlotSpace(0, 1200)
    appls = applications.generate_applications(1000, slotspace)

    graph_coloring(slotspace, appls)

if __name__ == "__main__":
    main()

