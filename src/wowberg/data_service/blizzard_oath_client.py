"""Blizzard API OAuth2 client for authenticated regional requests.

This module provides a small retrieval client for the Battle.net
client-credentials flow and regional Blizzard REST endpoints.

Usage:
    from data_service.blizzard_client import BlizzardOAuthClient

    client = BlizzardOAuthClient(client_id, client_secret, region="us")
    data = client.api_get("/data/wow/realm/index")

The client caches access tokens in memory until shortly before expiration.
"""
from __future__ import annotations
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from debug.debug import create_debug


import time
from typing import Optional, Dict, Any

# HTTP client for authenticated Blizzard API requests.
import requests
from authlib.integrations.requests_client import OAuth2Session



## Credientials for Blizzard API access
# Note: Secret stuff :)
# Default Blizzard application credentials used when callers do not supply overrides.
DEFAULT_CLIENT_ID = "09c055d763e848a4a251dbd61ab0eefd"
# Default Blizzard application secret used when callers do not supply overrides.
DEFAULT_CLIENT_SECRET = "Dj9NAoMQaC8xm1yZJaRqiF4RYqUZ2OAT"

# Debug tool
debug = create_debug([sys.stdout])

    
class BlizzardAuthError(RuntimeError):
    """Domain error for Blizzard OAuth and API request failures."""

    MESSAGE = "Authentification failed with Blizzard API"
    def __init__(self, message: Optional[str] = MESSAGE):
        super().__init__(message)

    
class BlizzardRegions:
    """Constants for Blizzard API regions."""
    US = "us"
    EU = "eu"
    KR = "kr"
    TW = "tw"

class BlizzardOAuthClient:
    """Blizzard API client that encapsulates token and endpoint handling.

    Contract:
    - Construct with `client_id`, `client_secret`, and an optional `region`.
    - Call `api_get()` with a Blizzard path to receive parsed JSON.
    - Use `fetch_token()` when callers need the raw OAuth token payload.

    Methods:
    - __init__(self, client_id, client_secret, region="us", scope=None): store client configuration.
    - fetch_token(self, region=None): request and cache an OAuth access token.
    - api_get(self, path, params=None, region=None): issue an authenticated GET request and return JSON.
    """
    def __init__(
        self,
        client_id: str = DEFAULT_CLIENT_ID,
        client_secret: str = DEFAULT_CLIENT_SECRET,
        region: BlizzardRegions = BlizzardRegions.US,
        scope: Optional[str] = None,
    ):
        """Initialize the Blizzard API client.

        Args:
            client_id (str): Blizzard application client ID. Defaults to the bundled client ID.
            client_secret (str): Blizzard application client secret. Defaults to the bundled client secret.
            region (BlizzardRegions): Blizzard API region, such as ``us`` or ``eu``.
            scope (Optional[str]): Optional OAuth scope string.
        """
        self._token: Optional[Dict[str, Any]] = None
        self._client_id = client_id
        self._client_secret = client_secret
        self._region = region
        self._expires_at: float = 0.0

    def fetch_token(self) -> Dict[str, Any]:
        """Fetch and cache a client-credentials token.

        Returns:
            Dict[str, Any]: Raw OAuth token response.

        Raises:
            BlizzardAuthError: If the token request fails.
        """
        if not self._region:
            raise BlizzardAuthError("BLIZZARD_INVALID_REGION")

        url = f"https://{self._region}.oauth.battle.net/token"
        try:
            oauth = OAuth2Session(client_id=self._client_id, client_secret=self._client_secret)
            token = oauth.fetch_token(url=url, grant_type="client_credentials")
            self._token = token
        except Exception as exception:  # keep broad to wrap external library errors
            raise BlizzardAuthError(f"BLIZZARD_TOKEN_FETCH_FAILED: {exception}")

        # Calculate expiration time for the token cache.
        expires_in = token.get("expires_in")
        if expires_in:
            self._expires_at = time.time() + int(expires_in) - 10
        else:
            # Fallback: use expires_at if provided or assume 1 hour.
            self._expires_at = float(token.get("expires_at", time.time() + 3600))

        if "access_token" not in token:
            raise BlizzardAuthError("BLIZZARD_TOKEN_MISSING_ACCESS_TOKEN") # This should never happen if the request succeeded, but we check to be safe.
        
        return token

    def _ensure_token(self) -> str:
        """Return a valid access token, refreshing it when needed."""
        if self._token and time.time() < self._expires_at:
            return self._token["access_token"]
        self._token = self.fetch_token()
        return self._token["access_token"]

__all__ = ["BlizzardOAuthClient", "BlizzardAuthError"]
