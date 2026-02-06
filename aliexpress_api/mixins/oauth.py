"""OAuth authentication mixin for AliExpress API.

DEPRECATED: This mixin is kept for backward compatibility only.
Use the service-based API instead:
    >>> api = AliexpressApi(KEY, SECRET)
    >>> api.oauth.generate_access_token(code="...")

Note: When using AliexpressApi, the mixin methods delegate to the
OAuthService which provides the same functionality.
"""

from .. import models


class OAuthMixin:
    """Mixin providing OAuth authentication methods.

    DEPRECATED: Use api.oauth instead of inheriting from this mixin.
    """

    def generate_access_token(
        self, code: str, uuid: str = None
    ) -> models.TokenResponse:
        """Generate an access token using the OAuth authorization code.

        Delegates to self.oauth.generate_access_token().
        """
        return self.oauth.generate_access_token(code=code, uuid=uuid)

    def refresh_access_token(self, refresh_token: str) -> models.TokenResponse:
        """Refresh an expired access token.

        Delegates to self.oauth.refresh_access_token().
        """
        return self.oauth.refresh_access_token(refresh_token=refresh_token)
