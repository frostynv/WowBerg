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
from wowberg.debug.debug import DebugInterface


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


class BlizzardRegions:
    """Constants for Blizzard API regions."""

    US = "us"
    EU = "eu"
    KR = "kr"
    TW = "tw"


class BlizzardOAuthClient(DebugInterface):
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
    ):
        """Initialize the Blizzard API client.

        Args:
            client_id (str): Blizzard application client ID. Defaults to the bundled client ID.
            client_secret (str): Blizzard application client secret. Defaults to the bundled client secret.
            region (BlizzardRegions): Blizzard API region, such as ``us`` or ``eu``.
        """
        self._token: str = None
        self._client_id = client_id
        self._client_secret = client_secret
        self._region = region

    def authenticate(self) -> str:
        """Fetch and cache a client-credentials token.

        Returns:
            str: OAuth token string.

        Raises:
            BlizzardAuthError: If the token request fails.
        """
        if not self._region:
            raise self.BlizzardInvalidRegion("BLIZZARD_INVALID_REGION")

        url = f"https://{self._region}.oauth.battle.net/token"
        try:
            oauth = OAuth2Session(
                client_id=self._client_id, client_secret=self._client_secret
            )
            token = oauth.fetch_token(url=url, grant_type="client_credentials")
            self._token = token
        except Exception as e:  # keep broad to wrap external library errors
            raise self.BlizzardAPIError(description=f"HTTP request failed: {e}")
        return token

    def _ensure_token(self) -> str:
        """Return a valid access token, refreshing it when needed."""
        if self.is_connected():
            return self._token  # valid token, don't fetch new one

        self._token = self.authenticate()
        return self._token

    def is_connected(self) -> bool:
        """Check if the client has a valid token."""
        try:
            response = requests.post(
                "https://oauth.battle.net/check_token",
                params={":region": self._region, "token": self._token},
                timeout=5,
            )
        except Exception as e:
            # raise all exceptions as BlizzardAPIError to unify error handling for callers
            raise self.BlizzardAPIError(description=f"HTTP request failed: {e}")

        # 405: Method Not Allowed (bad api usage)
        if response.status_code == 405:
            raise self.BlizzardMethodNotAllowedError(
                description=f"Invalid HTTP method used for Blizzard API endpoint: {response}"
            )
        # 400: Bad Request (invalid token, could be expired or malformed)
        elif response.status_code == 400:
            if response.json().get("error") == "invalid_token":
                return False
            else:
                raise self.BlizzardAPIError(
                    description=f"Unexpected error response returning same status code as invalid token: {response}"
                )
        # 200: OK (valid token)
        elif response.status_code == 200:
            return True
        else:
            raise self.BlizzardAPIError(
                description=f"Unexpected response from Blizzard when checking token validity: {response}",
            )


    class BlizzardAuthError(RuntimeError):
        """Domain error for Blizzard OAuth token retrieval failures."""

        MESSAGE = "General authentication error with Blizzard API"

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


    class BlizzardInvalidTokenException(BlizzardAuthError):
        """Domain error for Blizzard OAuth and API request failures.
        This is raised when the provided token is invalid or expired."""

        MESSAGE = "Authentication failed with token provided to Blizzard API"

        def __init__(
            self,
            message: Optional[str] = MESSAGE,
            description: Optional[str] = None,
            error_level: DebugInterface.ErrorLevels = DebugInterface.ErrorLevels.WARN,
        ):
            self.error_level = error_level
            super().__init__(message, description, error_level)


__all__ = [
    "BlizzardOAuthClient",
    "BlizzardInvalidTokenException",
    "BlizzardAuthError",
    "BlizzardRegions",
]
