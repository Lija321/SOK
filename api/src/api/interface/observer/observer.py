from abc import ABC, abstractmethod

class Observer(ABC):
    """
    Abstract Observer interface for the Observer pattern.
    
    Observers implement this interface to receive notifications
    when the state of an Observable object changes.
    """

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """
        Called when the observed object's state changes.
        
        :param observable: The observable object that triggered the update
        :type observable: Observable
        :param args: Additional positional arguments passed by the observable
        :param kwargs: Additional keyword arguments passed by the observable
        """
        pass