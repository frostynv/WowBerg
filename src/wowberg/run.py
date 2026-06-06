"""Main entrypoint for non-HTTP startup tasks."""

import requests

from wowberg.blizzard_oath_client import BlizzardOAuthClient, BlizzardRegions
from wowberg.services.auction import AuctionDataService
from wowberg.debug.debug import DebugInterface

LOCALE = "en_US"


class WowBerg(DebugInterface):
    def run_wowberg(self) -> None:
        """Run the Blizzard client startup flow."""

        self.debugger.log("Starting WowBerg application", prefix=DebugInterface.ErrorLevels.INFO)

        try:
            self.run_blizzard_client()
            self.debugger.log("WowBerg startup flow completed successfully.", prefix=DebugInterface.ErrorLevels.INFO)
        except Exception as e:
            self.debugger.log(f"Error occurred: {e}", prefix=DebugInterface.ErrorLevels.CRITICAL)

    def run_blizzard_client(self) -> None:
        """Fetch and log the Blizzard OAuth token."""
        blizzard_client = BlizzardOAuthClient(region=BlizzardRegions.US)

        try:
            token = blizzard_client.fetch_token()
        except Exception as e:
            self.debugger.log(f"Token Service: {e}", prefix=DebugInterface.ErrorLevels.CRITICAL)
            return

        # second test fetching from auction data
        auction_service = AuctionDataService(client=blizzard_client)
        try:
            auction_service.fetch_data(
                region=BlizzardRegions.US, realm_name="ursin"
            )
        except Exception as e:
            self.debugger.log(
                f"Auction Service: {e}", prefix=DebugInterface.ErrorLevels.CRITICAL
            )
            return


        with open("data.json", "w", encoding="utf-8") as file:
            file.write(auction_service._data)

        
        self.debugger.log(f"Blizzard client shutdown ({token})", prefix=DebugInterface.ErrorLevels.INFO)
        

    def print_json(self, data: dict) -> None:
        """Pretty-print a JSON dictionary."""
        import json

        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    # wowberg = WowBerg()
    # wowberg.run_wowberg()
    pass
