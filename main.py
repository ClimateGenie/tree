import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.generators import social


def find_index(strings, l):
    if len(strings[0]) > l:
        return 0
    running_sum = 0
    for i, s in enumerate(strings):
        running_sum += len(s)
        if running_sum > l:
            return (
                i - 1
            )  # return the previous index because this is the largest index with a sum less than l
    return (
        len(strings) - 1
    )  # if sum of all strings is less than l, return the last index


def format_label(label, return_length=9):
    if len(label) <= return_length:
        return label
    else:
        return_string = ""
        words = label.split(" ")
        while len(words):
            i = find_index(words, return_length)
            return_string += " ".join(words[: i + 1]) + "\n"
            words = words[i + 1 :]
        return return_string[:-1]


class Node:
    def __init__(self, name, color="red", graph=None, size=300):
        self.name = name
        self.color = color
        self.size = size
        self.graph = nx.DiGraph() if graph is None else graph
        self.graph.add_node(self.name, color=self.color, size=self.size)

    def connect(self, node):
        self.graph.add_edge(self.name, node.name)

    def create_child(self, name, color=None, size=300):
        if color:
            child_color = color
        else:
            child_color = self.color
        child = Node(name, child_color, self.graph, size)
        self.connect(child)
        return child

    def draw_graph(self):
        fig = plt.figure(1, figsize=(18, 9), dpi=300)
        ax = fig.add_subplot(111)
        ax.axis("off")
        pos = graphviz_layout(self.graph, prog="dot")

        colors = [
            color for name, color in nx.get_node_attributes(self.graph, "color").items()
        ]

        sizes = [
            size for name, size in nx.get_node_attributes(self.graph, "size").items()
        ]
        # nodes
        nx.draw_networkx_nodes(self.graph, pos, node_color=colors, node_size=sizes)

        # edges
        nx.draw_networkx_edges(
            self.graph,
            pos,
            edgelist=self.graph.edges(),
            arrows=True,
        )

        # Modify node labels to include newline after every 9 characters
        labels = {node: format_label(node, 9) for node in self.graph.nodes()}

        # labels
        nx.draw_networkx_labels(self.graph, pos, labels=labels, font_size=2.5)

        plt.savefig("tree.png", format="PNG")


def main():
    pre_release = Node("Pre Relsease", size=600, color="grey")

    pre_release_reqs = []
    admin = pre_release.create_child("Admin", "green")
    for req in [
        "Fact Checker Language Usage",
        "Signoff from Legal",
        "Signoff from marketing",
    ]:
        child = admin.create_child(req)
        pre_release_reqs.append(child)

    marketing = pre_release.create_child("Marketing", "cyan")
    for req in ["Update Socials", "Promo Materials"]:
        child = marketing.create_child(req)
        pre_release_reqs.append(child)

    technical = pre_release.create_child("Technical", "magenta")
    for req in ["Confirm Scalability", "Move off AWS"]:
        child = technical.create_child(req)
        pre_release_reqs.append(child)

    release = Node(
        "Relsease Climate Genie", color="Yellow", graph=pre_release.graph, size=600
    )
    for req in pre_release_reqs:
        req.connect(release)

    model = release.create_child("Model", "red")

    model.create_child("Other languages")
    ci = model.create_child("Classification Improvements")
    ci.create_child("Change Base Model")
    ci.create_child("More Labeling")
    inf_speed = ci.create_child("Better Inferance Speed")
    active_cache = inf_speed.create_child("Active Pre Caching of articles")

    taxonomy = model.create_child("Improve Taxonomy")

    taxonomy.create_child("Remove Un-used or Redundant Claims")

    l1 = taxonomy.create_child("New Level 1 Claims")

    l1.create_child("Green Washing Level 1 Claim")

    taxonomy.create_child("New Level 2 Claims")
    taxonomy.create_child("New Level 3 Claims")
    taxonomy.create_child("New Level 4 Claims")

    deploy = release.create_child("Deployment Methods", "Lime")
    deploy.create_child("Website (12ft.io Style)")
    deploy.create_child("App")
    deploy.create_child("Chatbot")
    social_media = deploy.create_child("Social Media Integration")
    social_media.create_child("Facebook")
    social_media.create_child("X")
    social_media.create_child("Instagram")
    social_media.create_child("Youtube")

    rnp = release.create_child("Research and Publications", "coral")
    accademic = rnp.create_child("Academic")
    accademic.create_child("Tracking Habit Change Through User Data")
    accademic.create_child("Replication of Coan 2021 with new model")
    accademic.create_child("Documentation of the extention design")

    deconstrution = accademic.create_child("Deconstrution of new claims")
    taxonomy.connect(deconstrution)

    reporting = rnp.create_child("Report Style")
    per_outlet = reporting.create_child("Per Outlet Performance Report")
    trending = reporting.create_child("Trending Misinformation")
    trending.create_child("Per Country")

    active_cache.connect(trending)

    partnerships = release.create_child("Partnerships", "dodgerblue")

    partnerships.create_child("Educators")
    partnerships.create_child("Fact Checkers")

    producers = partnerships.create_child("Publishers")

    per_outlet.connect(producers)

    pre_release.draw_graph()


if __name__ == "__main__":
    main()
