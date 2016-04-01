import networkx as nx
import matplotlib.pyplot as plt

def construct_graph(current_node,g,children_of):
    if current_node in children_of:
        for child in children_of[current_node]:
            g.add_node(child)
            g.add_edge(current_node,child)
            construct_graph(child,g,children_of)




def visualize_terms(root,nodes_in_collection,children_of):
    g = nx.DiGraph()
    g.add_node(root)
    construct_graph(root,g,children_of)
    colors = []
    for node in g.nodes():
        if node in nodes_in_collection:
            colors.append("blue")
        else:
            colors.append("white")
    pos = nx.spring_layout(g,scale=2)
    nx.draw(g,pos,node_color=colors,with_labels=True,font_size=14)
    plt.show()
