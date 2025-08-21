from .filter import Filter

from api.model import Graph
from api.services import DataSourcePlugin
from api.interface.observer import Observer

from typing import Set
from copy import deepcopy

class Workspace(Observer):

    """
    Workspace class that holds a collection of filters, the graph, and the data_source_plugin.
    """

    def __init__(self, data_source_plugin: DataSourcePlugin, name: str = "New Workspace"):
        """
        Initialize the workspace with an empty list of filters.
        """
        self._filters: Set[Filter] = set()
        self._data_source_plugin: DataSourcePlugin = data_source_plugin
        self._graph: Graph = self._data_source_plugin.load_data()
        self._graph.attach(self)
        # Initialize the rendered graph (no filters applied initially)
        self.__filtered_graph: Graph = self.__filter_graph()


    @property
    def filters(self) -> Set[Filter]:
        """
        Get the list of filters in the workspace.

        :return: The list of filters
        :rtype: list[Filter]
        """
        return self._filters

    @property
    def graph(self) -> Graph:
        """
        Get the graph in the workspace, which is the filtered version of the original graph.
        :return: The filtered graph
        :rtype: Graph
        """
        return self.__filtered_graph

    @property
    def graph_reference(self) -> Graph:
        """
        Get the original graph reference (unfiltered).

        :return: The original graph reference
        :rtype: Graph
        """
        return self._graph

    def add_filter(self, filter_) -> Set[Filter]:
        """
        Add a filter to the workspace.

        :param filter_: The filter to add
        :type filter_: Filter

        :raises ValueError: If the filter is already in the workspace
        :return: The updated list of filters
        :rtype: Set[Filter]
        Returns the updated set of filters so that the caller can chain calls or check the current filters.
        """
        if not isinstance(filter_, Filter):
            raise TypeError(f"Expected a Filter instance, got {type(filter_).__name__}")
        
        self._filters.add(filter_)
        # Update the rendered graph with the new filter applied
        self.__filtered_graph = self.__filter_graph()

        return self._filters

    def remove_filter(self, filter_) -> Set[Filter]:
        """
        Remove a filter from the workspace.
        :param filter_: The filter to remove
        :type filter_: Filter

        :raises ValueError: If the filter is not in the workspace
        :return: The updated list of filters
        :rtype: Set[Filter]
        Returns the updated set of filters so that the caller can chain calls or check the current filters.
        """
        if filter_ in self._filters:
            self._filters.remove(filter_)
            # Update the rendered graph after removing the filter
            self.__filtered_graph = self.__filter_graph()
        else:
            raise ValueError("Filter not found in workspace.")

        return self._filters

    def update(self, observable=None, *args, **kwargs) -> None:
        """
        Update the workspace when the graph changes.
        This method is called when the observed graph notifies its observers.
        
        :param observable: The observable object (typically the graph)
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        """
        # When the underlying graph changes, update the filtered graph
        if observable is self._graph:
            self.__filtered_graph = self.__filter_graph()

    def __filter_graph(self) -> Graph:
        """
        Apply all filters to the graph and return the filtered graph.
        This method should be called whenever a filter is added or removed.

        :return: The filtered graph
        :rtype: Graph
        """
        # If no filters are applied, return a deep copy of the original graph
        if not self._filters:
            return deepcopy(self._graph)
        
        # Start with all nodes and edges from the original graph
        filtered_nodes = set()
        filtered_edges = set()
        
        # Apply filters to nodes
        for node in self._graph.nodes:
            # A node passes if it satisfies ALL filters
            node_passes = True
            for filter_ in self._filters:
                try:
                    if not filter_.apply(node):
                        node_passes = False
                        break
                except (KeyError, TypeError, AttributeError):
                    # If filter can't be applied to this node (missing attribute, type mismatch, etc.)
                    # consider the node as not passing the filter
                    node_passes = False
                    break
            
            if node_passes:
                filtered_nodes.add(node)
        
        # Filter edges: include only edges where both origin and target nodes are in filtered nodes
        for edge in self._graph.edges:
            # An edge is included if both its origin and target nodes are in the filtered nodes set
            if edge.origin in filtered_nodes and edge.target in filtered_nodes:
                filtered_edges.add(edge)
        
        # Create and return the filtered graph
        filtered_graph = Graph(
            edges=filtered_edges, 
            nodes=filtered_nodes, 
            directed=self._graph.is_directed()
        )
        
        return filtered_graph    