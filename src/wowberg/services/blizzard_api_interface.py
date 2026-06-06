from abc import ABC, abstractmethod
from http import client
from pathlib import __all__
from typing import Optional

import requests

from wowberg.blizzard_oath_client import BlizzardRegions, BlizzardOAuthClient
from wowberg.debug.debug import DebugInterface

class BlizzardNamepaces:
    """Constants for Blizzard API namespaces."""
    PROFILE = "profile"
    STATIC = "static"
    DYNAMIC = "dynamic"

class BlizzardAPIInterface(ABC):
    """
    BlizzardAPIInterface defines the interface for a Blizzard API data provider.
    Functionalities:
    - Modular design to allow for different implementation of different type of data, such as price data, item information data, etc.
    - Fetching data for a given symbol.
    - Encapsulate error handling, data formatting, and configuration management related to specific data sources.
    """

    def __init__(self, client: BlizzardOAuthClient):
        # Initialize any necessary variables or connections here
        
        self.config: dict[str, object] = {
            "client": client,
        }
        
    @property
    def client(self) -> BlizzardOAuthClient:
        client: BlizzardOAuthClient | None = self.config["client"]
        if client is None:
            raise RuntimeError(
                "AuctionDataService requires a BlizzardOAuthClient in config"
            )
        return client
    
        
    def is_connected(self) -> bool:
        """
        Check if the data provider is connected to the data sources.

        Returns:
            bool: True if connected, False otherwise.
        """
        client: BlizzardOAuthClient | None = self.config["client"]
        # null check
        if client is None:
            return False
        return client.is_connected()
        
        
    @abstractmethod
    def fetch_data(self) -> bool:
        """
        Fetch data by implementing this method in the subclass.
        """
        pass

    def set_config(self, config: dict[str, object]) -> bool:
        """
        Set the configuration for the data provider.

        Args:
            config (dict): A dictionary containing configuration parameters.
        """
        self.config.update(config)
        return True
    
    class BlizzardAPIError(RuntimeError):
        """Domain unexpected error for Blizzard API service failures."""

        MESSAGE = "Unexpected error occured in Blizzard API Service."

        def __init__(
            self,
            message: Optional[str] = MESSAGE,
            description: Optional[str] = None,
            error_level: DebugInterface.ErrorLevels = DebugInterface.ErrorLevels.CRITICAL,
        ):
            super().__init__(message)
            self.error_level = error_level
            self.message = message
            self.description = description

    class BlizzardInvalidRegionException(BlizzardAPIError):
        """Domain error for invalid Blizzard API region."""

        MESSAGE = "Invalid Blizzard API region"

        def __init__(
            self,
            message: Optional[str] = MESSAGE,
            description: Optional[str] = None,
            error_level: DebugInterface.ErrorLevels = DebugInterface.ErrorLevels.CRITICAL,
        ):
            super().__init__(message, description, error_level)

    class BlizzardMethodNotAllowedError(BlizzardAPIError):
        """Domain error for invalid HTTP method usage with Blizzard API."""

        MESSAGE = "Invalid HTTP method used for Blizzard API endpoint"

        def __init__(
            self,
            message: Optional[str] = MESSAGE,
            description: Optional[str] = None,
            error_level: DebugInterface.ErrorLevels = DebugInterface.ErrorLevels.CRITICAL,
        ):
            super().__init__(message, description, error_level)
    
    class BlizzardUtils:
        @staticmethod
        def get_header_signature(token: str, namespace:str, region: BlizzardRegions) -> dict[str, str]:
            """
            Get the headers for the API request by inputing an token

            Args:
                token (str): The OAuth token for authentication.

            Returns:
                dict: A dictionary containing the headers for the API request.
            """
            header = {
                "Authorization": f"Bearer {token['access_token']}",
                "Battlenet-Namespace": f"{BlizzardAPIInterface.BlizzardUtils.get_region_namespace('dynamic', region)}"
            }
            return header
    
        @staticmethod  
        def get_region_namespace(type: str, region: BlizzardRegions) -> str:
            """
            Get the appropriate namespace for the API based on the region.

            Args:
                type (str): The type of namespace (e.g., "profile", "static", "dynamic").
                region (BlizzardRegions): The Blizzard region for which to determine the namespace.
            """
            
            return f"{type}-{region}"
        
        
        @staticmethod
        def url(region: BlizzardRegions) -> str:
            """Return the realm endpoint URL for the provided region and realm id."""
            return f"https://{region}.api.blizzard.com/data/wow/"
        
        

__all__ = ["BlizzardAPIInterface", "BlizzardNamepaces", "BlizzardAPIError", "BlizzardInvalidRegionException", "BlizzardMethodNotAllowedError"]