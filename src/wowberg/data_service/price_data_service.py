from wowberg.data_service.game_data_interface import DataProviderInterface

class PriceDataService(DataProviderInterface):
    
    config: dict[str, object] = {
        "token": None
            
        
    }
    
    def __init__(self):
        pass

    def is_connected(self) -> bool:
        return False

    def fetch_data(self) -> bool:
        return False
    def set_config(self, config: dict[str, object]) -> bool:
        return False