from .facotry_abs import FactoryPlacaAbs
from placa import PlacaSlave


class FactoryPlacaSlave(FactoryPlacaAbs):

    def create_placa(self, name):
        return PlacaSlave(name)