from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.security.auth import (
    AuthenticationError,
    validate_token,
)

from app.security.models import CurrentUser


security = HTTPBearer(
    auto_error=False,
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            )
    print("\n========== AUTH HEADER ==========")
    print(credentials)
    print("=================================\n")


    try:

        claims = await validate_token(
            credentials.credentials
        )

        return CurrentUser(
            id=claims.get("oid") or claims["sub"],
            name=claims.get("name"),
            email=claims.get("preferred_username"),
            roles=claims.get("roles", []),
        )

    except AuthenticationError as ex:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex),
        ) from ex