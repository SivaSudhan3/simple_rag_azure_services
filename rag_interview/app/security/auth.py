from __future__ import annotations

import jwt

from jwt import (
    PyJWKClient,
    ExpiredSignatureError,
    InvalidAudienceError,
    InvalidIssuerError,
    InvalidTokenError,
)

from rag_interview.core.config.config import entrasettings


class AuthenticationError(Exception):
    """Raised when authentication fails."""


TENANT_ID = entrasettings.ENTRA_TENANT_ID

JWKS_URL = (
    f"https://login.microsoftonline.com/"
    f"{TENANT_ID}/discovery/v2.0/keys"
)

# Accept both Entra ID v1 and v2 issuers
VALID_ISSUERS = [
    f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
    f"https://sts.windows.net/{TENANT_ID}/",
]

REQUIRED_SCOPE = "chat.access"

_jwk_client = PyJWKClient(JWKS_URL)


def _get_signing_key(token: str):
    return _jwk_client.get_signing_key_from_jwt(token).key


async def validate_token(token: str) -> dict:

    try:

        signing_key = _get_signing_key(token)

        # Disable issuer verification here because we'll validate
        # against both supported issuers manually.
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=entrasettings.ENTRA_AUDIENCE,
            options={
                "verify_iss": False,
            },
        )

        issuer = payload.get("iss")

        if issuer not in VALID_ISSUERS:
            raise AuthenticationError("Invalid issuer")

        scopes = payload.get("scp", "").split()

        if REQUIRED_SCOPE not in scopes:
            raise AuthenticationError(
                f"Missing required scope: {REQUIRED_SCOPE}"
            )

        return payload

    except ExpiredSignatureError as ex:
        raise AuthenticationError("Token has expired") from ex

    except InvalidAudienceError as ex:
        raise AuthenticationError("Invalid audience") from ex

    except InvalidTokenError as ex:
        raise AuthenticationError("Invalid token") from ex