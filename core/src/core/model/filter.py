from api.model.const import DataValue
from api.model import Edge, Node, Graph
from .base_filter import BaseFilter
from typing import Optional, Union

class Filter(BaseFilter):

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

    def __init__(self, attribute: str, value: DataValue = None, operator: str = None, graph: Optional[Graph] = None):
        """
        Initialize the filter with a specific attribute.

        :param attribute: The attribute to filter on
        :type attribute: str
        :param value: The value to filter with
        :type value: DataValue
        :param operator: The operator to use for filtering
        :type operator: str
        :param graph: Optional graph reference for type validation
        :type graph: Optional[Graph]
        """
        self._attribute = attribute
        self._value = value
        self._operator = operator

        if operator not in self.OPERATORS:
            raise ValueError(f"Invalid operator: {operator}. Valid operators are: {list(self.OPERATORS.keys())}")

        if value is not None and not isinstance(value, DataValue):
            raise TypeError(f"Value must be of type DataValue, got {type(value)} instead.")

        # Type validation using graph's attribute type information
        if graph is not None and attribute in graph.attribute_types:
            expected_type = graph.get_attribute_type(attribute)
            if not isinstance(value, expected_type):
                # Handle Union types (when an attribute can have multiple types)
                if hasattr(expected_type, '__origin__') and expected_type.__origin__ is Union:
                    # Check if the value type is one of the union types
                    union_types = expected_type.__args__
                    if not any(isinstance(value, t) for t in union_types):
                        raise TypeError(f"Value type {type(value).__name__} does not match expected type(s) {expected_type.__name__} for attribute '{attribute}'")
                else:
                    raise TypeError(f"Value type {type(value).__name__} does not match expected type {expected_type.__name__} for attribute '{attribute}'")

        self.__key = self.OPERATORS[operator]

    @property
    def attribute(self) -> str:
        """
        Get the attribute name for template access.
        :return: The attribute name
        :rtype: str
        """
        return self._attribute

    @property
    def operator(self) -> str:
        """
        Get the operator for template access.
        :return: The operator
        :rtype: str
        """
        return self._operator

    @property
    def value(self) -> DataValue:
        """
        Get the value for template access.
        :return: The value
        :rtype: DataValue
        """
        return self._value

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

    def __eq__(self, other) -> bool:
        """
        Check equality between two Filter instances based on their attributes.
        
        :param other: Another Filter instance to compare with
        :return: True if both filters have the same attribute, operator, and value, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Filter):
            return False
        return (self._attribute == other._attribute and 
                self._operator == other._operator and 
                self._value == other._value)

    def __hash__(self) -> int:
        """
        Hash function for the Filter instance based on its attributes.
        
        :return: Hash value based on attribute, operator, and value
        :rtype: int
        """
        return hash((self._attribute, self._operator, self._value))

    def __str__(self) -> str:
        """
        String representation of the Filter instance.
        
        :return: String representation of the filter
        :rtype: str
        """
        return f"Filter(attribute={self._attribute}, operator={self._operator}, value={self._value})"

    def __repr__(self) -> str:
        """
        Official string representation of the Filter instance.
        
        :return: Official string representation of the filter
        :rtype: str
        """
        return self.__str__()
