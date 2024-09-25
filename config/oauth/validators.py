from itertools import chain

from django.conf import settings
from oauth2_provider.oauth2_validators import OAuth2Validator

_permissions_as_tuples = list(
    chain.from_iterable([role["permissions"] for role in settings.ROLES])
)

REQUESTED_PERMISSIONS = [".".join(perm) for perm in _permissions_as_tuples]


class CustomOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = OAuth2Validator.oidc_claim_scope
    oidc_claim_scope.update({"permissions": "permissions"})
    oidc_claim_scope.update({"permission_name": "profile"})

    def get_additional_claims(self, request):
        current_permissions = list(request.user.get_all_permissions())

        try:
            if request.user.photo is not None:
                image = request.user.photo.url
            else:
                image = None

        except ValueError:
            image = None

        return {
            "given_name": request.user.first_name,
            "family_name": request.user.last_name,
            "name": " ".join([request.user.first_name, request.user.last_name]),
            "preferred_username": request.user.username,
            "email": request.user.email,
            "picture": image,
            "permissions": [
                perm for perm in current_permissions if perm in REQUESTED_PERMISSIONS
            ],
            "permission_name": request.user.groups.first(),
        }

    def get_userinfo_claims(self, request):
        claims = super().get_userinfo_claims(request)
        # noinspection PyUnresolvedReferences
        claims["email"] = request.user.email
        return claims
