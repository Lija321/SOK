from .base_filter import BaseFilter
from api.model.const import DataValue
from api.model import Edge, Node

class Search(BaseFilter):

    """
    Search class for the Search pattern.

    Searches implement this interface to process data in a specific way.
    """

    def __init__(self, value: DataValue):
        """
        Initialize the search with a specific value.
        :param value: The value to search for
        :type value: DataValue
        """
        # Call parent constructor with search-specific defaults
        # No type validation is performed for Search since it has different logic
        self._value = value

    @property
    def value(self) -> DataValue:
        """
        Get the value to search for.
        :return: The value to search for
        :rtype: DataValue
        """
        return self._value

    @value.setter
    def value(self, value: DataValue):
        """
        Set the value to search for.
        :param value: The value to search for
        :type value: DataValue
        """
        self._value = value

    def apply(self, comparable: Node | Edge) -> bool:
        """
        Apply the search to a Node or Edge.
        :param comparable: The Node or Edge to search
        :type comparable: Node | Edge
        :return: True if the Node or Edge matches the search, False otherwise
        """
        if not isinstance(comparable, (Node, Edge)):
            raise TypeError(f"Comparable must be of type Node or Edge, got {type(comparable)} instead.")

        for attr, val in comparable.data.items():
            if attr == self._value:
                return True
            if val == self._value:
                return True
        
        # Return False if no matches found
        return False

    def __eq__(self, other) -> bool:
        """
        Check equality between two Search instances based on their values.
        
        :param other: Another Search instance to compare with
        :return: True if both searches have the same value, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Search):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        """
        Hash function for the Search instance based on its value.
        
        :return: Hash value of the search's value
        :rtype: int
        """
        return hash(self._value) if self._value is not None else 0

    def __str__(self) -> str:
        """
        String representation of the Search instance.
        
        :return: String representation of the search
        :rtype: str
        """
        return f"Search(value={self._value})"

    def __repr__(self) -> str:
        """
        Official string representation of the Search instance.
        
        :return: Official string representation of the search
        :rtype: str
        """
        return self.__str__()