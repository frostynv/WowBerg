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


class BlizzardAuthError(RuntimeError):
    pass


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
        region: str = "us",
        scope: Optional[str] = None,
    ):
        """Initialize the Blizzard API client.

        Args:
            client_id (str): Blizzard application client ID. Defaults to the bundled client ID.
            client_secret (str): Blizzard application client secret. Defaults to the bundled client secret.
            region (str): Blizzard API region, such as ``us`` or ``eu``.
            scope (Optional[str]): Optional OAuth scope string.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.scope = scope

        self._token: Optional[Dict[str, Any]] = None
        self._expires_at: float = 0.0

    def _token_url(self) -> str:
        """Build the OAuth token endpoint URL."""
        return f"https://oauth.battle.net/token"

    def _api_base(self, region: str) -> str:
        """Build the Blizzard REST API base URL for a region."""
        return f"https://{region}.api.blizzard.com"

    def fetch_token(self, region: Optional[str] = None) -> Dict[str, Any]:
        """Fetch and cache a client-credentials token.

        Args:
            region (Optional[str]): Region override for the token request.

        Returns:
            Dict[str, Any]: Raw OAuth token response.

        Raises:
            BlizzardAuthError: If the token request fails.
        """
        region = region or self.region
        token_url = self._token_url()

        try:
            oauth = OAuth2Session(client_id=self.client_id, client_secret=self.client_secret)
            token = oauth.fetch_token(token_url=token_url, grant_type="client_credentials")
        except Exception as exc:  # keep broad to wrap external library errors
            raise BlizzardAuthError(f"failed to fetch token: {exc}") from exc

        # calc expiry
        expires_in = token.get("expires_in")
        if expires_in:
            self._expires_at = time.time() + int(expires_in) - 10
        else:
            # fallback: use expires_at if provided or assume 1 hour
            self._expires_at = float(token.get("expires_at", time.time() + 3600))

        self._token = token
        return token

    def _ensure_token(self) -> str:
        """Return a valid access token, refreshing it when needed."""
        if self._token and time.time() < self._expires_at:
            return self._token["access_token"]
        token = self.fetch_token()
        return token["access_token"]

    def api_get(self, path: str, params: Optional[Dict[str, Any]] = None, region: Optional[str] = None) -> Any:
        """Perform an authenticated GET request against Blizzard API.

        Args:
            path (str): Blizzard resource path, with or without a leading slash.
            params (Optional[Dict[str, Any]]): Optional query string parameters.
            region (Optional[str]): Region override for the API request.

        Returns:
            Any: Parsed JSON response body.

        Raises:
            BlizzardAuthError: If the HTTP request fails.
        """
        region = region or self.region
        base = self._api_base(region)
        url = base.rstrip("/") + "/" + path.lstrip("/")

        access_token = self._ensure_token()
        headers = {"Authorization": f"Bearer {access_token}"}

        resp = requests.get(url, headers=headers, params=params)
        try:
            resp.raise_for_status()
        except requests.HTTPError as exc:
            # surface as a domain error for callers to handle
            raise BlizzardAuthError(f"Blizzard API request failed: {exc} - {resp.text}") from exc

        return resp.json()


__all__ = ["BlizzardOAuthClient", "BlizzardAuthError"]
