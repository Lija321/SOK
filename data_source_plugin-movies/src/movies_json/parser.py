from typing import Dict, Set
from api.model import Node, Edge


def create_nodes(data: Dict, only_films: bool = False, min_rating: float = None) -> Set[Node]:
    """
    Create Node objects from JSON.
    """
    nodes = set()
    for node in data["nodes"]:
        if only_films and node.get("type") != "film":
            continue
        if min_rating and node.get("type") == "film" and node.get("rating", 0) < min_rating:
            continue

        n = Node(id=node["id"], data=node)
        nodes.add(n)
    return nodes


def create_edges(data: Dict, nodes: Set[Node], **kwargs) -> Set[Edge]:
    """
    Create Edge objects from JSON.
    """
    edges = set()
    node_dict = {n.id: n for n in nodes}

    for edge in data["edges"]:
        source_id = edge["from"]
        target_id = edge["to"]

        if source_id in node_dict and target_id in node_dict:
            source_node = node_dict[source_id]
            target_node = node_dict[target_id]
            e = Edge(source_node, target_node, data={**edge, "type": edge.get("relationType")})
            edges.add(e)

    return edges
