from typing import Optional


class Author(object):
    def __init__(self, 
                 id: str, 
                 first_name: str, 
                 last_name: str, 
                 email: Optional[str] = None, 
                 affiliation: Optional[str] = None,
                 initials: Optional[str] = None):
        self.__id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__affiliation = affiliation
        self.__initials = initials

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        if isinstance(value, str):
            self.__id = value
        else:
            raise TypeError('Value must be type of str')

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        if isinstance(value, str):
            self.__first_name = value
        else:
            raise TypeError('Value must be type of str')

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        if isinstance(value, str):
            self.__last_name = value
        else:
            raise TypeError('Value must be type of str')

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__email = value

    @property
    def affiliation(self):
        return self.__affiliation

    @affiliation.setter
    def affiliation(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__affiliation = value

    @property
    def initials(self):
        return self.__initials

    @initials.setter
    def initials(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__initials = value

    @property
    def full_name(self):
        return f"{self.__first_name} {self.__last_name}".strip()

    @property
    def last_first_name(self):
        """Format as 'Last, First' for citations."""
        return f"{self.__last_name}, {self.__first_name}".strip(', ')

    @property
    def initials_name(self):
        """Format with initials if available."""
        if self.__initials:
            return f"{self.__initials} {self.__last_name}".strip()
        else:
            # Generate initials from first name
            first_initial = self.__first_name[0] + '.' if self.__first_name else ''
            return f"{first_initial} {self.__last_name}".strip()

    def __str__(self):
        return self.full_name
