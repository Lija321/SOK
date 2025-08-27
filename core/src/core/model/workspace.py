import uuid
from functools import wraps

from .filter import Filter

from api.model import Graph
from api.services import DataSourcePlugin
from api.interface.observer import Observer

from typing import Set, Union
from copy import deepcopy
from datetime import date


def parse_filter(func):
    """
    A decorator for the add and remove filter methods to parse a filter string into a Filter object.
    
    This decorator allows the methods to accept either a Filter object or a filter string.
    If a string is provided, it will be parsed into a Filter object.
    
    :param func: The function to decorate
    :return: The decorated function
    """
    @wraps(func)
    def wrapper(self, filter_):
        # If filter_ is already a Filter object, use it directly
        if isinstance(filter_, Filter):
            return func(self, filter_)
        
        # If filter_ is a string, parse it into a Filter object
        if isinstance(filter_, str):
            print("Parsing filter string:", filter_)
            parsed_filter = _parse_filter_string(filter_)
            return func(self, parsed_filter)
        
        # If filter_ is neither Filter nor string, raise an error
        raise TypeError(f"Expected Filter instance or str, got {type(filter_).__name__}")
    
    return wrapper


def _parse_filter_string(filter_string: str) -> Filter:
    """
    Parse a filter string into a Filter object.

    :param filter_string: The filter string to parse (format: "attribute operator value")
    :type filter_string: str
    :return: The parsed Filter object
    :rtype: Filter
    """
    # Example filter string format: "attribute operator value"
    try:
        attribute, operator, value = filter_string.split(" ", 2)
    except ValueError:
        raise ValueError("Filter string must be in the format 'attribute operator value'")

    # Convert value to appropriate type (int, float, str)
    original_value = value
    
    # Try to convert to int first
    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        value = int(value)
    # Try to convert to float
    elif '.' in value and value.replace('.', '').replace('-', '').isdigit():
        try:
            value = float(value)
        except ValueError:
            value = original_value  # Keep as string if conversion fails
    # Check for boolean values
    elif value.lower() in ['true', 'false']:
        value = value.lower() == 'true'
    else:
        # Try to parse as date
        try:
            value = date.fromisoformat(value)
        except ValueError:
            # Keep as string if not a date
            pass

    return Filter(attribute=attribute, operator=operator, value=value)


class Workspace(Observer):

    """
    Workspace class that holds a collection of filters, the graph, and the data_source_plugin.
    """

    def __init__(self,
                 data_source_plugin: DataSourcePlugin,
                 name: str = "New Workspace",
                 visualizer_id: str|None = None):
        """
        Initialize the workspace with an empty list of filters.
        """
        self.id = str(uuid.uuid4())
        self._filters: Set[Filter] = set()
        self._data_source_plugin: DataSourcePlugin = data_source_plugin
        self._graph: Graph = self._data_source_plugin.load_data()
        self.visualizer_id = visualizer_id
        self._graph.attach(self)
        # Initialize the rendered graph (no filters applied initially)
        self.__filtered_graph: Graph = self.__filter_graph()
        self.name = name


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

    @parse_filter
    def add_filter(self, filter_) -> Set[Filter]:
        """
        Add a filter to the workspace.

        :param filter_: The filter to add (can be a Filter object or a filter string)
        :type filter_: Filter | str

        :raises ValueError: If the filter is already in the workspace
        :raises TypeError: If the filter is neither a Filter instance nor a string
        :return: The updated list of filters
        :rtype: Set[Filter]
        Returns the updated set of filters so that the caller can chain calls or check the current filters.
        """
        self._filters.add(filter_)
        # Update the rendered graph with the new filter applied
        self.__filtered_graph = self.__filter_graph()

        return self._filters

    @parse_filter
    def remove_filter(self, filter_) -> Set[Filter]:
        """
        Remove a filter from the workspace.
        
        :param filter_: The filter to remove (can be a Filter object or a filter string)
        :type filter_: Filter | str

        :raises ValueError: If the filter is not in the workspace
        :raises TypeError: If the filter is neither a Filter instance nor a string
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
