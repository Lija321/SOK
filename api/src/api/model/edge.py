from typing import Optional

from api.model import Node
from typing import Dict
from copy import deepcopy
from api.model.const import DataValue

class Edge(object):

    def __init__(self, origin: Node, target: Node, data: Optional[Dict[str, DataValue]] = None ):
        """
        Initialize an Edge instance.

        :param origin: The originating Node of the edge.
        :param target: The target Node of the edge.
        """
        self._origin = origin
        self._target = target
        self._data: Dict[str, DataValue] = data


    @property
    def origin(self) -> Node:
        """
        Get the originating Node of the edge.

        :return: The originating Node.
        :rtype: Node
        """
        return self._origin

    @property
    def target(self) -> Node:
        """
        Get the target Node of the edge.

        :return: The target Node.
        :rtype: Node
        """
        return self._target

    @origin.setter
    def origin(self, value: Node):
        """
        Set the originating Node of the edge.

        :param value: The originating Node.
        """
        self._origin = value

    @target.setter
    def target(self, value: Node):
        """
        Set the target Node of the edge.

        :param value: The target Node.
        """
        self._target = value

    @property
    def data(self) -> Dict[str, DataValue]:
        """
        Get the data associated with the edge.

        :return: The data dictionary.
        :rtype: Dict[str, DataValue]
        """
        return self._data

    @data.setter
    def data(self, value: Dict[str, DataValue]):
        """
        Set the data associated with the edge.

        :param value: The data dictionary.
        """
        self._data = value if value is not None else {}

    def __eq__(self, other):
        """
        Check equality of two Edge instances.

        :param other: Another Edge instance to compare with.
        :return: True if both edges have the same origin and target, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Edge):
            return False
        return self.origin == other.origin and self.target == other.target

    def __str__(self):
        """
        String representation of the Edge instance.

        :return: A string describing the edge.
        :rtype: str
        """
        return f"Edge from {self.origin.id} to {self.target.id}"

    def __repr__(self):
        """
        Representation of the Edge instance.

        :return: A string representation of the edge.
        :rtype: str
        """
        return self.__str__()

    def __hash__(self):
        """
        Hash function for the Edge instance.

        :return: Hash value based on the origin and target IDs.
        :rtype: int
        """
        return hash((self.origin.id, self.target.id))

    def deep_copy(self, node_mapping: Dict[str, Node] = None) -> 'Edge':
        """
        Create a deep copy of this Edge instance.
        
        :param node_mapping: Optional mapping from node IDs to copied Node instances.
                           If provided, will use existing copied nodes instead of creating new ones.
                           This is useful for maintaining node identity in graph copying.
        :type node_mapping: Dict[str, Node]
        :return: A new Edge instance with deep-copied nodes and data.
        :rtype: Edge
        """
        # If node mapping is provided, use it to get copied nodes
        if node_mapping is not None:
            copied_origin = node_mapping.get(self._origin.id)
            copied_target = node_mapping.get(self._target.id)
            
            # If nodes are not in mapping, create copies and add them
            if copied_origin is None:
                copied_origin = self._origin.deep_copy()
                node_mapping[self._origin.id] = copied_origin
            if copied_target is None:
                copied_target = self._target.deep_copy()
                node_mapping[self._target.id] = copied_target
        else:
            # Create new copies of the nodes
            copied_origin = self._origin.deep_copy()
            copied_target = self._target.deep_copy()
        
        # Create a deep copy of the data dictionary
        copied_data = deepcopy(self._data) if self._data is not None else None
        
        # Create a new Edge instance with the copied nodes and data
        return Edge(origin=copied_origin, target=copied_target, data=copied_data)

    def __deepcopy__(self, memo) -> 'Edge':
        """
        Magic method for Python's copy.deepcopy() function.
        This allows copy.deepcopy(edge) to use our custom deep copy logic.
        
        Note: When using copy.deepcopy() on an individual edge, we cannot maintain
        node identity across multiple edges. For that, use Graph.deep_copy() instead.
        
        :param memo: Dictionary used by deepcopy to track copied objects (prevents infinite recursion)
        :return: A new Edge instance with deep-copied nodes and data.
        :rtype: Edge
        """
        return self.deep_copy()
