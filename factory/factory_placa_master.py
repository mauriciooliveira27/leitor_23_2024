from .factory_abs import FactoryPlacaAbs
from placa import PlacaMaster



class FactoryPlacaMaster(FactoryPlacaAbs):

    def create_placa(self):
        return PlacaMaster()