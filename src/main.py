"""Main entrypoint for non-HTTP startup tasks."""

import sys

from data_service.blizzard_client import BlizzardOAuthClient
from debug.debug import create_debug


debug = create_debug([sys.stdout])


def main() -> None:
    """Run the Blizzard client startup flow."""
    run_blizzard_client()


def run_blizzard_client() -> None:
    """Fetch and log the Blizzard OAuth token."""

    debug.log("Starting Blizzard API client using bundled credentials", prefix="[DIV]")
    
    blizzard_client = BlizzardOAuthClient()
    token = blizzard_client.fetch_token()
    debug.log(f"Blizzard API returned token: {token}", prefix="[ATT]")


if __name__ == "__main__":
    main()
