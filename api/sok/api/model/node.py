from typing import Dict, Any, Optional, List
from api.sok.api.model.const import DataValue

class Node(object):
    """
    Represents a node in a graph structure.
    Each node has a unique identifier and associated data.
    """

    def __init__(self, id: str, data: Dict[str, DataValue]):
        """
        Initialize a Node instance.

        :param id: Unique identifier for the node.
        :param data: Dictionary containing node data.
        """
        self._id = id
        self._data = data

    @property
    def id(self) -> str:
        """
        Get the unique identifier of the node.

        :return: Unique identifier of the node.
        :rtype: str
        """
        return self._id

    @property
    def data(self) -> Dict[str, DataValue]:
        """
        Get the data associated with the node.

        :return: Dictionary containing node data.
        :rtype: Dict[str, Any]
        """
        return self._data

    @id.setter
    def id(self, value: str):
        """
        Set the unique identifier of the node.

        :param value: Unique identifier for the node.
        """
        self._id = value

    @data.setter
    def data(self, value: Dict[str, DataValue]):
        """
        Set the data associated with the node.

        :param value: Dictionary containing node data.
        """
        self._data = value

    def __eq__(self, other: 'Node') -> bool:
        """
        Check equality between two Node instances based on their IDs.

        :param other: Another Node instance to compare with.
        :return: True if both nodes have the same ID, False otherwise.
        :rtype: bool
        """
        return self.id == other.id

    def __str__(self):
        """
        String representation of the Node instance.

        :return: String representation of the node.
        :rtype: str
        """
        return f"Node(id={self.id}, data={self.data})"

    def __repr__(self):
        """
        Official string representation of the Node instance.

        :return: Official string representation of the node.
        :rtype: str
        """
        return self.__str__()

    def __hash__(self):
        return hash(self._id)