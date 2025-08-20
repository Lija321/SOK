from .filter import Filter

from api.model import Graph
from api.services import DataSourcePlugin
from api.interface.observer import Observer

from typing import Set

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

    @property
    def filters(self) -> Set[Filter]:
        """
        Get the list of filters in the workspace.

        :return: The list of filters
        :rtype: list[Filter]
        """
        return self._filters

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

        #TODO: apply filter to the graph
        self._filters.add(filter_)

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
        else:
            raise ValueError("Filter not found in workspace.")

        return self._filters

    def update(self) -> None:
        """
        Update the workspace when the graph changes.
        """
        pass