from api.services import Plugin
from api.model import Graph

from abc import abstractmethod


class DataSourcePlugin(Plugin):
    """
    Abstract base class for data source plugins.
    """

    @abstractmethod
    def load_data(self, **kwargs) -> Graph:
        """
        Load data from the data source.

        This method should be implemented by subclasses to load data from the specific data source.
        """
        pass
