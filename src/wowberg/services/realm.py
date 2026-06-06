from wowberg.services.blizzard_api_interface import (
    BlizzardAPIInterface,
)
from wowberg.blizzard_oath_client import BlizzardOAuthClient, BlizzardRegions
from wowberg.debug.debug import DebugInterface
import requests


class RealmDataService(BlizzardAPIInterface, DebugInterface):

    config: dict[str, object] = {
        "client": None,
    }

    data: dict[str, object] = {"data": None}

    def __init__(self, client: BlizzardOAuthClient):
        self.config["client"] = client

    def fetch_connect_realm_id(
        self,
        region: BlizzardRegions = BlizzardRegions.US,  # default to US region TODO: remove in release
        realm_name: str = "ursin",  # default to Ursin realm TODO: remove in release
    ) -> str:
        """Fetch realm data and return the connected-realm ID."""
        self.debugger.log(f"{self.client._ensure_token()}")
        request_url = f"{BlizzardAPIInterface.BlizzardUtils.url(region=region)}/realm/{realm_name}"
        request_headers = (
            BlizzardAPIInterface.BlizzardUtils.get_header_signature(
                token=self.client._ensure_token(),
                namespace="dynamic",
                region=region,
            )
        )
        request_params = {
            "locale": "en_US",
        }

        try:
            response = requests.get(
                request_url,
                headers=request_headers,
                params=request_params,
                timeout=20,
            )
        except Exception as e:
            self.debugger.log(
                f"Error occurred while making realm API request: {e}",
                prefix="[ERR]",
            )
            return None

        """
        {'_links': {'self': {'href': 'https://us.api.blizzard.com/data/wow/realm/ursin?namespace=dynamic-us'}}, 'id': 156, 'region': {'key': {'href': 'https://us.api.blizzard.com/data/wow/region/1?namespace=dynamic-us'}, 'name': 'North America', 'id': 1}, 'connected_realm': {'href': 'https://us.api.blizzard.com/data/wow/connected-realm/96?namespace=dynamic-us'}, 'name': 'Ursin', 'category': 'United States', 'locale': 'enUS', 'timezone': 'America/New_York', 'type': {'type': 'NORMAL', 'name': 'Normal'}, 'is_tournament': False, 'slug': 'ursin'}"""

        try:
            response = requests.get(
                response.json()["connected_realm"]["href"],
                headers=request_headers,
                timeout=20,
            )
        except Exception as e:
            self.debugger.log(
                f"Error occurred while making connected realm API request: {e}",
                prefix="[ERR]",
            )
            return None

        return response.json().get("id")

    def fetch_data(
        self,
        region: BlizzardRegions = BlizzardRegions.US,
        realm_id: str = "156",
    ) -> dict[str, object]:
        """Compatibility wrapper for interface contract."""
        return {
            "connected_realm_id": self.fetch_connect_realm_id(
                region=region, realm_id=realm_id
            )
        }

    def set_config(self, config: dict[str, object]) -> bool:
        return False
