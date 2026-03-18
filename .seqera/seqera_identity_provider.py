from typing import Union, Any
from dataclasses import asdict
from urllib.parse import unquote
import base64
import json

from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.auth import IdentityProvider, User


class SeqeraIdentityProvider(IdentityProvider):
    """Seqera Identity Provider for Jupyter"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log = kwargs.get('log')

    @staticmethod
    def username_initials(username: str):
        """Creates the username initials based on the given username"""

        splits = username.upper().split(' ')
        if len(splits) < 2:
            return splits[0][0]
        return splits[0][0]+splits[-1][0]

    @staticmethod
    def decode_id_token(cookie: str | None) -> Union[dict, None]:
        """Decodes the idtoken set in the cookie and returns the decoded claims.
        It doesn't validate that the jwt is valid, assuming this has been validated
        already by the connect proxy"""
        if cookie is None:
            return None
        tokens = unquote(cookie).split('\t')
        if len(tokens) != 2:
            return None
        segments = tokens[1].split('.')
        if len(segments) != 3:
            return None

        # add padding to value to make sure decoding works, additional padding will be ignored
        data = json.loads(str(base64.urlsafe_b64decode(segments[1] + '==='), 'utf-8'))
        return data

    def get_user(self, handler: JupyterHandler) -> Union[User, None]:
        user_data = SeqeraIdentityProvider.decode_id_token(handler.get_cookie('connect-auth-tokens'))
        if user_data is None:
            return None

        # try to get a username from the extracted claims
        user_name = user_data.get('preferred_username', None)
        if user_name is None:
            user_name = user_data.get('name', None)
        if user_name is None:
            user_name = user_data.get('email', None)
        if user_name is None:
            return None

        initials = SeqeraIdentityProvider.username_initials(user_name)

        usr = User(username=user_name,
                   name=user_name,
                   display_name=user_name,
                   initials=initials
                   )
        return usr

    def identity_model(self, user: User) -> dict[str, Any]:
        return asdict(user)



# Configure jupyter lab to use the identity provider
c = get_config() # type: ignore[name-defined]
c.ServerApp.identity_provider_class = SeqeraIdentityProvider