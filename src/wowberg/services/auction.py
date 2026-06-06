from wowberg.services.blizzard_api_interface import (
    BlizzardAPIInterface,
)
from wowberg.services.realm import RealmDataService
from wowberg.blizzard_oath_client import BlizzardOAuthClient, BlizzardRegions
from wowberg.debug.debug import DebugInterface
import requests


class AuctionDataService(BlizzardAPIInterface, DebugInterface):

    def __init__(self, client: BlizzardOAuthClient):
        super().__init__(client=client)
        self._data: str = None

    def fetch_data(
        self,
        region: BlizzardRegions = BlizzardRegions.US,
        realm_name: str = "ursin",
    ):
        """Fetch auction data for the specified region and realm ID."""
        connected_realm_id = RealmDataService(client=self.client).fetch_connect_realm_id(
            region=region,
            realm_name=realm_name,
        )

        request_param = {
            "locale": "en_US",
        }
        request_url = f"{BlizzardAPIInterface.BlizzardUtils.url(region=region)}/connected-realm/{connected_realm_id}/auctions"
        request_headers = BlizzardAPIInterface.BlizzardUtils.get_header_signature(
            token=self.client._ensure_token(),
            namespace="dynamic",
            region=region,
        )
        
        self.debugger.log(f"Auction API request URL: {request_url}", prefix=DebugInterface.ErrorLevels.TEST)
        self.debugger.log(f"Auction API request headers: {request_headers}", prefix=DebugInterface.ErrorLevels.TEST)
        
        try:
            response = requests.get(
                url=request_url,
                headers=request_headers,
                params=request_param,
                timeout=20,
            )
        except Exception as e:
            self.debugger.log(f"Error while fetching auction data: {e}", prefix=DebugInterface.ErrorLevels.CRITICAL)
            return None


        # 405: Method Not Allowed (bad api usage)
        if response.status_code == 405:
            raise BlizzardAPIInterface.BlizzardMethodNotAllowedError(f"BLIZZARD_METHOD_NOT_ALLOWED {response}")
        # 400: Bad Request (invalid token, could be expired or malformed)
        elif response.status_code == 400:
            raise BlizzardOAuthClient.BlizzardInvalidTokenException(f"BLIZZARD_TOKEN_CHECK_BAD_REQUEST {response}")
        # 200: OK (valid token)
        elif response.status_code == 200:
            self._data = response.text
        else:
            self.debugger.log(f": {response}", prefix=DebugInterface.ErrorLevels.WARN)
            raise BlizzardAPIInterface.BlizzardAPIError(f"BLIZZARD_UNKNOWN_RESPONSE: {response}")
