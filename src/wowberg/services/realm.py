from wowberg.services.blizzard_api_interface import (
    BlizzardAPIInterface,
)
from wowberg.blizzard_oath_client import BlizzardOAuthClient, BlizzardRegions
from wowberg.logger.service import LogService
import requests


class RealmDataService(BlizzardAPIInterface):

    config: dict[str, object] = {
        "client": None,
    }

    def __init__(self, client: BlizzardOAuthClient):
        super().__init__(client=client)
        self.config["client"] = client

    def get_connect_realm_id(
        self,
        region: BlizzardRegions = BlizzardRegions.US,  # default to US region TODO: remove in release
        realm_name: str = "ursin",  # default to Ursin realm TODO: remove in release
    ) -> str:
        """Fetch realm data and return the connected-realm ID."""
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
            LogService.log(
                f"Error occurred while making realm API request: {e}",
                prefix="[ERR]",
            )
            return None

        try:
            response = requests.get(
                response.json()["connected_realm"]["href"],
                headers=request_headers,
                timeout=20,
            )
        except Exception as e:
            LogService.log(
                f"Error occurred while making connected realm API request: {e}",
                prefix="[ERR]",
            )
            return None

        return response.json().get("id")

    def set_config(self, config: dict[str, object]) -> bool:
        return False
