from api.model.const import DataValue

class Filter(object):

    """
    Abstract Filter class for the Filter pattern.

    Filters implement this interface to process data in a specific way.
    """

    OPERATORS = {
    "==": "",
    "!=": "",
    "<": "",
    "<=": "",
    ">": "",
    ">=": "",
    "contains": "",
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