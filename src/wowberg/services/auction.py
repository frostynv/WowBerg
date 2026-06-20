from wowberg.services.blizzard_api_interface import (
    BlizzardAPIInterface,
)
from wowberg.services.realm import RealmDataService
from wowberg.blizzard_oath_client import BlizzardOAuthClient, BlizzardRegions
from wowberg.logger.logservice import LogService
import requests
from datetime import datetime, timedelta, timezone


class AuctionDataService(BlizzardAPIInterface):

    def __init__(self, client: BlizzardOAuthClient):
        super().__init__(client=client)

    def is_modified(
        self,
        region: BlizzardRegions = BlizzardRegions.US,
        realm_name: str = "ursin",
    ) -> bool:
        """Check if the auction data has been modified since the last fetch."""
        connected_realm_id = RealmDataService(
            client=self.client
        ).get_connect_realm_id(
            region=region,
            realm_name=realm_name,
        )

        request_param = {
            "locale": "en_US",
        }
        request_url = f"{BlizzardAPIInterface.BlizzardUtils.url(region=region)}/connected-realm/{connected_realm_id}/auctions"
        request_headers = (
            BlizzardAPIInterface.BlizzardUtils.get_header_signature(
                token=self.client._ensure_token(),
                namespace="dynamic",
                region=region,
            )
        )

    @property
    def data_region(self) -> BlizzardRegions:
        """Return the region associated with the currently stored auction data."""
        return self._data.get("region", None)

    @property
    def data_realm(self) -> str:
        """Return the realm name associated with the currently stored auction data."""
        return self._data.get("realm", None)

    @property
    def data_last_modified(self, format: str = "%Y-%m-%dT%H-%M-%S") -> str:
        """Return the timestamp of when the auction data was last modified."""
        last_modified = self._data.get("last_modified", None)
        if last_modified:
            return datetime.strptime(
                last_modified.isoformat(), "%Y-%m-%dT%H:%M:%S.%f"
            ).strftime(format)
        return None

    def update_all_auctions(
        self,
        region: BlizzardRegions = BlizzardRegions.US,
        realm_name: str = "ursin",
        cached: bool = False,
    ):
        """Fetch or update auction data for the specified region and realm."""
        connected_realm_id = RealmDataService(
            client=self.client
        ).get_connect_realm_id(
            region=region,
            realm_name=realm_name,
        )

        request_param = {
            "locale": "en_US",
        }
        request_url = f"{BlizzardAPIInterface.BlizzardUtils.url(region=region)}/connected-realm/{connected_realm_id}/auctions"
        request_headers = (
            BlizzardAPIInterface.BlizzardUtils.get_header_signature(
                token=self.client._ensure_token(),
                namespace="dynamic",
                region=region,
            )
        )

        if cached and self._data.get("last_modified", None) is not None:
            mock_last_modified = datetime.now(timezone.utc) - timedelta(
                minutes=1
            )
            formated_time = mock_last_modified.strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            )
            request_headers.update({"if-modified-since": formated_time})

        try:
            response = requests.get(
                url=request_url,
                headers=request_headers,
                params=request_param,
                timeout=20,
            )
        except Exception as e:
            LogService.log(
                f"Error while fetching auction data: {e}",
                prefix=LogService.ErrorLevels.CRITICAL,
                handler="blizzard",
            )
            return None

        # 405: Method Not Allowed (bad api usage)
        if response.status_code == 405:
            raise BlizzardAPIInterface.BlizzardMethodNotAllowedError(
                f"BLIZZARD_METHOD_NOT_ALLOWED {response}"
            )
        # 400: Bad Request (invalid token, could be expired or malformed)
        elif response.status_code == 400:
            raise BlizzardOAuthClient.BlizzardInvalidTokenException(
                f"BLIZZARD_TOKEN_CHECK_BAD_REQUEST {response}"
            )

        elif response.status_code == 304:
            LogService.log(
                f"BLIZZARD_AUCTIONS_NOT_MODIFIED {realm_name} ({region}).",
                prefix=LogService.ErrorLevels.INFO,
                handler="blizzard",
            )
            return None
        # 200: OK (valid token)
        elif response.status_code == 200:
            self._data = {
                "data": response.text,
                "last_modified": datetime.now(),
                "realm": realm_name,
                "region": region,
            }
        else:
            LogService.log(
                f"BLIZZARD_UNKNOWN_RESPONSE: {response}",
                prefix=LogService.ErrorLevels.WARN,
                handler="blizzard",
            )
            raise BlizzardAPIInterface.BlizzardAPIError(
                f"BLIZZARD_UNKNOWN_RESPONSE: {response}"
            )
