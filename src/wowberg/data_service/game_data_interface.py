from abc import ABC, abstractmethod
from pathlib import __all__


class DataProviderInterface(ABC):
    """
    DataProviderInterface defines the interface for a market data provider.
    Functionalities:
    - Modular design to allow for different implementation of different type of data, such as price data, item information data, etc.
    - Fetching data for a given symbol.
    - Encapsulate error handling, data formatting, and configuration management related to specific data sources.
    """

    def __init__(self):
        # Initialize any necessary variables or connections here
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if the data provider is connected to the data sources.

        Returns:
            bool: True if connected, False otherwise.
        """
        pass

    @abstractmethod
    def fetch_data(self) -> bool:
        """
        Fetch data by
        """

    @abstractmethod
    def set_config(self, config: dict[str, object]) -> bool:
        """
        Set the configuration for the data provider.

        Args:
            config (dict): A dictionary containing configuration parameters.
        """
        pass 


__all__ = ["DataProviderInterface"]