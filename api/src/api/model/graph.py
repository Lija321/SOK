from typing import Optional, Set, Dict
from api.model import Node, Edge
from api.interface.observer import Observable

class Graph(Observable):
    """A class representing a graph structure."""

    def __init__(self, edges: Optional[Set[Edge]] = None, nodes: Optional[Set[Node]] = None,
                 directed: Optional[bool] = True):
        """
        Initialize a Graph instance.

        :param edges: A collection of Edge instances representing the edges of the graph.
        :type edges: Optional[Set[Edge]]
        :param nodes: A collection of Node instances representing the nodes of the graph.
        :type nodes: Optional[Set[Node]]
        :param directed: A boolean indicating whether the graph is directed (default is True).
        :type directed: Optional[bool]
        """
        super().__init__()
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

    def deep_copy(self, copy_observers: bool = False) -> 'Graph':
        """
        Create a deep copy of this Graph instance.
        
        :param copy_observers: If True, also copies the observers attached to this graph.
                              If False (default), the new graph will have no observers.
        :type copy_observers: bool
        :return: A new Graph instance with deep-copied nodes and edges.
        :rtype: Graph
        """
        # Create a mapping to ensure node identity is preserved across edges
        node_mapping: Dict[str, Node] = {}
        
        # First, create copies of all nodes
        copied_nodes = set()
        for node in self._nodes:
            copied_node = node.deep_copy()
            node_mapping[node.id] = copied_node
            copied_nodes.add(copied_node)
        
        # Then, create copies of all edges using the node mapping
        copied_edges = set()
        for edge in self._edges:
            copied_edge = edge.deep_copy(node_mapping)
            copied_edges.add(copied_edge)
        
        # Create the new graph with copied data
        new_graph = Graph(edges=copied_edges, nodes=copied_nodes, directed=self._directed)
        
        # Optionally copy observers
        if copy_observers:
            # Note: We copy the observer references, not deep copy the observers themselves
            # This is because observers are typically external objects that shouldn't be duplicated
            for observer in self._observers:
                new_graph.attach(observer)
        
        return new_graph

    def __deepcopy__(self, memo) -> 'Graph':
        """
        Magic method for Python's copy.deepcopy() function.
        This allows copy.deepcopy(graph) to use our custom deep copy logic.
        
        Note: When using copy.deepcopy(), observers are not copied by default.
        Use graph.deep_copy(copy_observers=True) if you need to copy observers.
        
        :param memo: Dictionary used by deepcopy to track copied objects (prevents infinite recursion)
        :return: A new Graph instance with deep-copied nodes and edges.
        :rtype: Graph
        """
        return self.deep_copy(copy_observers=False)







