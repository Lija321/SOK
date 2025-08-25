from typing import Optional, Set, Dict, Any
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
        print("Graph before:", [n.id for n in self._nodes])
        self._nodes.add(node)
        self.notify(action="add_node", node=node)
        print("Graph after:", [n.id for n in self._nodes])

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
        self.notify(action="add_edge", edge=edge)

    def get_node(self, node_id: str) -> Optional[Node]:
        """Return the node with the given ID, or None if it doesn't exist."""
        for node in self._nodes:
            if node.id == node_id:
                return node
        return None

    def get_edge(self, origin_id: str, target_id: str) -> Optional[Edge]:
        """Return the edge from origin_id to target_id, or None if it doesn't exist."""
        for edge in self._edges:
            if edge.origin.id == origin_id and edge.target.id == target_id:
                return edge
        return None

    def remove_node(self, node_id: str):
        """Remove a node by ID if it exists and has no connected edges; raise ValueError otherwise."""
        node = self.get_node(node_id)
        if not node:
            raise ValueError(f"Node {node_id} not found.")
        if any(edge.origin == node or edge.target == node for edge in self._edges):
            raise ValueError(f"Cannot delete node {node_id}, it has connected edges.")
        self._nodes.remove(node)
        self.notify(action="remove_node", node=node)

    def remove_edge(self, origin_id: str, target_id: str):
        """Remove an edge by origin and target node IDs; raise ValueError if not found."""
        edge = self.get_edge(origin_id, target_id)
        if not edge:
            raise ValueError(f"Edge from {origin_id} to {target_id} not found.")
        self._edges.remove(edge)
        self.notify(action="remove_edge", edge=edge)

    def is_directed(self) -> bool:
        """Return True if the graph is directed, False otherwise."""
        return self._directed

    def update_node(self, node_id: str, properties: Dict[str, Any]):
        """Update properties of the node with the given ID; raise ValueError if node not found."""
        node = self.get_node(node_id)
        if not node:
            raise ValueError(f"Node {node_id} not found.")
        node.update_properties(properties)
        self.notify(action="update_node", node=node, properties=properties)

    def update_edge(self, origin_id: str, target_id: str, properties: Dict[str, Any]):
        """Update properties of the edge from origin_id to target_id; raise ValueError if edge not found."""
        edge = self.get_edge(origin_id, target_id)
        if not edge:
            raise ValueError(f"Edge from {origin_id} to {target_id} not found.")
        edge.update_properties(properties)
        self.notify(action="update_edge", edge=edge, properties=properties)

    def clear(self):
        """Remove all nodes and edges from the graph and notify observers."""
        self._nodes.clear()
        self._edges.clear()
        self.notify(action="clear_graph")

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







