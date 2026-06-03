"""Main entrypoint for non-HTTP startup tasks."""

import sys

import requests

from wowberg.data_service.blizzard_oath_client import BlizzardOAuthClient, BlizzardRegions
from debug.debug import create_debug


debug = create_debug([sys.stdout])
LOCALE = "en_US"


def run_wowberg() -> None:
    """Run the Blizzard client startup flow."""
    
    debug.log("Starting WowBerg application")
    
    try:
        run_blizzard_client()
    except Exception as e:
        debug.log(f"Error occurred: {e}", prefix="[ERR]")


def run_blizzard_client() -> None:
    """Fetch and log the Blizzard OAuth token."""
    blizzard_client = BlizzardOAuthClient(region=BlizzardRegions.US)
    token = blizzard_client.fetch_token()

    url = "https://us.api.blizzard.com/profile/wow/character/ursin/sojourner"
    debug.log(f"Making API request to {url} with token: {token['access_token']}")
    params = {
        "namespace": "profile-us",   # character data must use profile namespace
        "locale": LOCALE,
    }
    
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    resp = requests.get(url, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    print(resp.json())

        
        
if __name__ == "__main__":
    run_wowberg()
    
    