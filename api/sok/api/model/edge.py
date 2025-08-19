from api.sok.api.model import Node

class Edge(object):

    def __init__(self, origin: Node, target: Node):
        """
        Initialize an Edge instance.

        :param origin: The originating Node of the edge.
        :param target: The target Node of the edge.
        """
        self._origin = origin
        self._target = target

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
        return hash((self._origin, self._target))
