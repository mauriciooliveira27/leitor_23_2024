from abc import ABC, abstractmethod

from placa import PlacaSlave, PlacaMaster



class FactoryPlacaAbs(ABC):

    @abstractmethod
    def create_placa(self):
        pass



