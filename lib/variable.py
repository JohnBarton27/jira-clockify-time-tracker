import os


class Variable:

    def __init__(self, name: str, value: str = None):
        """
        Constructor for Variable object, which pulls variables from the environment.

        Args:
            name (str): Name of the environment variable
            value (str): Value of the environment variable (Default: None)
        """
        self.name = name
        self._value = value

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @property
    def value(self):
        """
        Property for the value of the Variable. If not given in the __init__, gets the value from the environment.

        Returns:
            str: Value of the environment variable
        """
        if self._value:
            return self._value

        return os.getenv(self.name)
