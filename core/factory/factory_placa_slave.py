from .factory_abs import FactoryPlacaAbs
from placa import PlacaSlave


class FactoryPlacaSlave(FactoryPlacaAbs):

    def create_placa(self,ip_placa, cod_placa):
        return PlacaSlave(ip_placa, cod_placa)