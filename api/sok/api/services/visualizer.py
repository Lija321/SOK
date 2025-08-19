from api.sok.api.model import Graph
from api.sok.api.services import Plugin
from abc import ABC, abstractmethod

class Visualizer(Plugin,ABC):

    @abstractmethod
    def identifier(self) -> str:
        pass
    @abstractmethod
    def display_graph(self,graph: Graph) -> None:
        pass