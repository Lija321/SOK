from typing import List
from abc import abstractmethod, ABC
from citations.api.model import Citation


class Plugin(ABC):
    @abstractmethod
    def name(self) -> str:
        """
        Retrieves the name of the citation data source plugin.

        :return: The name of the citation data source plugin.
        :rtype: str
        """
        pass

    @abstractmethod
    def identifier(self) -> str:
        """
        Retrieves a unique identifier for the citation data source plugin.

        :return: The unique identifier of the citation data source plugin.
        :rtype: str
        """
        pass


class DataSourcePlugin(Plugin):
    """
    An abstraction representing a plugin for loading citation data from a specific data source.
    """

    @abstractmethod
    def load(self, **kwargs) -> List[Citation]:
        """
        Loads citation data from the data source and returns it as a list of `Citation` objects.

        :param kwargs: Arbitrary keyword arguments for customization or filtering of the data loading process.
        :type kwargs: dict
        :return: A list of `Citation` objects loaded from the data source.
        :rtype: List[Citation]
        """
        pass

    @abstractmethod
    def search(self, query: str, **kwargs) -> List[Citation]:
        """
        Searches for citations based on a query string.

        :param query: The search query string.
        :type query: str
        :param kwargs: Arbitrary keyword arguments for customization or filtering of the search process.
        :type kwargs: dict
        :return: A list of `Citation` objects matching the search criteria.
        :rtype: List[Citation]
        """
        pass

    @abstractmethod
    def get_by_id(self, citation_id: str, **kwargs) -> Citation:
        """
        Retrieves a specific citation by its ID.

        :param citation_id: The unique identifier of the citation.
        :type citation_id: str
        :param kwargs: Arbitrary keyword arguments for customization.
        :type kwargs: dict
        :return: The `Citation` object with the specified ID.
        :rtype: Citation
        :raises: Exception if citation not found.
        """
        pass
