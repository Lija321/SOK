from typing import Optional, Set
from api.model import Node, Edge

class Graph(object):
    """A class representing a graph structure."""

    def __init__(self, edges: Optional[Set[Edge]] = None, nodes: Optional[Set[Node]] = None, directed: Optional[bool] = True):
        """
        Initialize a Graph instance.

        :param edges: A collection of Edge instances representing the edges of the graph.
        :type edges: Optional[Set[Edge]]
        :param nodes: A collection of Node instances representing the nodes of the graph.
        :type nodes: Optional[Set[Node]]
        :param directed: A boolean indicating whether the graph is directed (default is True).
        :type directed: Optional[bool]
        """
        self._edges = edges if edges else set()
        self._nodes = nodes if nodes else set()
        self._directed = directed


    @property
    def edges(self) -> Set[Edge]:
        """
        Get the edges of the graph.

        :return: A set of Edge instances.
        :rtype: Set[Edge]
        """
        return self._edges

    @property
    def nodes(self) -> Set[Node]:
        """
        Get the nodes of the graph.

        :return: A set of Node instances.
        :rtype: Set[Node]
        """
        return self._nodes

    def add_node(self, node: Node) -> None:
        """
        Add a Node to the graph.

        :param node: The Node instance to add.
        :type node: Node
        """

        if not isinstance(node, Node):
            raise TypeError(f"Expected a Node instance, got {format(type(node).__name__)}")
        self._nodes.add(node)

    def add_edge(self, edge: Edge) -> None:
        """
        Add an Edge to the graph.

        :param edge: The Edge instance to add.
        :type edge: Edge
        """
        if not isinstance(edge, Edge):
            raise TypeError(f"Expected an Edge instance, got {format(type(edge).__name__)}")

        if edge in self._edges:
            return

        if self._directed:
            self._edges.add(edge)
        else:
            self._edges.add(Edge(edge.target, edge.origin))

        self._nodes.add(edge.origin)
        self._nodes.add(edge.target)

    def is_directed(self) -> bool:
        return self._directed






