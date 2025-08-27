from abc import ABC, abstractmethod
from api.model.const import DataValue
from api.model import Edge, Node


class BaseFilter(ABC):
    """
    Abstract base class for filtering and searching operations.
    
    This class defines the common interface that all filter-like classes should implement.
    """

    @abstractmethod
    def apply(self, comparable: Node | Edge) -> bool:
        """
        Apply the filter/search logic to a Node or Edge.

        This method should be implemented by subclasses to define their specific
        filtering or searching behavior.

        :param comparable: The Node or Edge to test
        :type comparable: Node | Edge
        :return: True if the Node or Edge matches the criteria, False otherwise
        :rtype: bool
        """
        pass
