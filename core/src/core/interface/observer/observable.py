from abc import ABC, abstractmethod
from typing import Set, List
from .observer import Observer


class Observable(ABC):
    """
    Abstract Observable interface for the Observer pattern.
    
    Observable objects maintain a list of observers and notify them
    when their state changes.
    """

    def __init__(self):
        """Initialize the observable with an empty set of observers."""
        self._observers: Set[Observer] = set()

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to this observable.
        
        :param observer: The observer to attach
        :type observer: Observer
        """
        if not isinstance(observer, Observer):
            raise TypeError("Observer must implement the Observer interface")
        self._observers.add(observer)

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from this observable.
        
        :param observer: The observer to detach
        :type observer: Observer
        """
        self._observers.discard(observer)

    def notify(self, *args, **kwargs) -> None:
        """
        Notify all attached observers of a state change.
        
        :param args: Additional positional arguments to pass to observers
        :param kwargs: Additional keyword arguments to pass to observers
        """
        for observer in self._observers.copy():  # Use copy to avoid modification during iteration
            try:
                observer.update(self, *args, **kwargs)
            except Exception as e:
                # Log the exception but continue notifying other observers
                print(f"Error notifying observer {observer.get_id()}: {e}")

    def get_observers(self) -> List[Observer]:
        """
        Get a list of all attached observers.
        
        :return: List of attached observers
        :rtype: List[Observer]
        """
        return list(self._observers)

