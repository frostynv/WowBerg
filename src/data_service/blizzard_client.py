"""Blizzard API OAuth2 client using Authlib.

Provides a small, testable client that performs the client-credentials
flow against Battle.net (Blizzard) and performs authenticated GET requests
to the regional Blizzard API.

Usage:
    from market_data_service.blizzard_client import BlizzardOAuthClient

    client = BlizzardOAuthClient(client_id, client_secret, region='us')
    data = client.api_get('/data/wow/realm/index')

The class caches the token in memory until shortly before expiration.
"""
from __future__ import annotations

import time
from typing import Optional, Dict, Any

import requests 
from authlib.integrations.requests_client import OAuth2Session


class BlizzardAuthError(RuntimeError):
    pass


class BlizzardOAuthClient:
    """Simple Blizzard API client using client_credentials via Authlib.

    Contract (smallest useful slice):
    - Construct with `client_id`, `client_secret`, and optional `region`.
    - `api_get(path, params=None, region=None)` returns parsed JSON from Blizzard.
    - Handles token retrieval and in-memory caching.
    """

    def __init__(self, client_id: str, client_secret: str, region: str = "us", scope: Optional[str] = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.scope = scope

        self._token: Optional[Dict[str, Any]] = None
        self._expires_at: float = 0.0

    def _token_url(self, region: str) -> str:
        return f"https://{region}.battle.net/oauth/token"

    def _api_base(self, region: str) -> str:
        return f"https://{region}.api.blizzard.com"

    def fetch_token(self, region: Optional[str] = None) -> Dict[str, Any]:
        region = region or self.region
        token_url = self._token_url(region)

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
        if self._token and time.time() < self._expires_at:
            return self._token["access_token"]
        token = self.fetch_token()
        return token["access_token"]

    def api_get(self, path: str, params: Optional[Dict[str, Any]] = None, region: Optional[str] = None) -> Any:
        """Perform a GET request against Blizzard API and return parsed JSON.

        `path` may be absolute (leading `/`) or relative; it will be joined to the
        regional API base, e.g. `https://us.api.blizzard.com`.
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
