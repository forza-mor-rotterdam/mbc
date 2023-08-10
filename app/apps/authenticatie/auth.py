from mozilla_django_oidc import auth


class OIDCAuthenticationBackend(auth.OIDCAuthenticationBackend):
    def create_user(self, claims):
        email = claims.get("email")
        user = self.UserModel.objects.create_user(email=email)

        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()

        return user

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()

        return user

    def get_userinfo(self, access_token, id_token, payload):
        """Return user details dictionary. The id_token and payload are not used in
        the default implementation, but may be used when overriding this method"""
        print(id_token)
        # print(self.get_payload_data(id_token))
        print(payload)
        # user_response = requests.get(
        #     self.OIDC_OP_USER_ENDPOINT,
        #     headers={"Authorization": "Bearer {0}".format(access_token)},
        #     verify=self.get_settings("OIDC_VERIFY_SSL", True),
        #     timeout=self.get_settings("OIDC_TIMEOUT", None),
        #     proxies=self.get_settings("OIDC_PROXY", None),
        # )
        # user_response.raise_for_status()
        return payload
