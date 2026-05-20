from game_data_interface import DataProviderInterface




class PriceDataService(DataProviderInterface):
    testVariable = 0
    def __init__(self):
        pass

    def is_connected(self) -> bool:
        return False

    def fetch_data(self) -> bool:
        return False
    def set_config(self, config: dict[str, str]) -> bool:
        return False