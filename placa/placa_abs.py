from abc import ABC , abstractmethod



class PlacaAbstract(ABC):

    @abstractmethod
    def read_temp(self, data_placa: object) -> dict:
        pass


