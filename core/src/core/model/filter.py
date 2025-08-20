from api.model.const import DataValue
from api.model import Edge, Node

class Filter(object):

    """
    Abstract Filter class for the Filter pattern.

    Filters implement this interface to process data in a specific way.
    """

    OPERATORS = {
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y
    }

    def __init__(self, attribute: str, value: DataValue = None, operator: str = None):
        """
        Initialize the filter with a specific attribute.

        :param attribute: The attribute to filter on
        :type attribute: str
        """
        self._attribute = attribute
        self._value = value
        self._operator = operator

        if operator not in self.OPERATORS:
            raise ValueError(f"Invalid operator: {operator}. Valid operators are: {list(self.OPERATORS.keys())}")

        if value is not None and not isinstance(value, DataValue):
            raise TypeError(f"Value must be of type DataValue, got {type(value)} instead.")

        self.__key = self.OPERATORS[operator]

    @property
    def attribute(self) -> str:
        """
        Get the attribute to filter on.

        :return: The attribute
        :rtype: str
        """
        return self._attribute

    @property
    def value(self) -> DataValue:
        """
        Get the value to filter on.

        :return: The value
        :rtype: DataValue
        """
        return self._value

    @property
    def operator(self) -> str:
        """
        Get the operator to filter with.

        :return: The operator
        :rtype: str
        """
        return self._operator

    def __eq__(self, other):
        """
        Check if two filters are equal based on their attributes, values, and operators.

        :param other: The other filter to compare with
        :type other: Filter
        :return: True if the filters are equal, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Filter):
            return False
        return (self.attribute == other.attribute and
                self.value == other.value and
                self.operator == other.operator)

    def __hash__(self):
        """
        Get the hash of the filter based on its attributes, values, and operators.

        :return: The hash of the filter
        :rtype: int
        """
        return hash((self.attribute, self.value, self.operator))


    def apply(self, comparable: Node | Edge) -> bool:
        """
        Call the filter to process data.

        This method should be implemented by subclasses to apply the filter logic.
        It should return a list of nodes or edges that match the filter criteria.

        :return: A list of nodes or edges that match the filter criteria
        :rtype: list[Node] | list[Edge]
        """
        comparable_value = comparable.data.get(self.attribute, None)
        if comparable_value is None:
            return False

        if(type(comparable_value) is not type(self.value)):
            raise TypeError(f"Type mismatch: {type(comparable_value)} vs {type(self.value)}")

        return self.__key(comparable_value, self.value)
