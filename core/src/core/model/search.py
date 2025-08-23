from .filter import Filter
from api.model.const import DataValue
from api.model import Edge, Node

class Search(Filter):

    """
    Search class for the Search pattern.

    Searches implement this interface to process data in a specific way.
    """

    # noinspection PyMissingConstructor
    # We don't call super().__init__ because we want to force value to be set; and attribute and operator are relevant
    def __init__(self, value: DataValue):
        """
        Initialize the search with a specific value.
        :param value: The value to search for
        :type value: DataValue
        """
        self._value = value
        self._attribute = ""
        self._operator = "contains"


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