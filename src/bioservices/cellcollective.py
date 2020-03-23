# imports - third-party imports
import requests

# imports - module imports
from bioservices.services import REST, BioServicesError
from bioservices._compat import string_types

__all__ = ["CellCollective", "CCAuthenticationError"]

class CCAuthenticationError(BioServicesError):
    pass

class CCAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    @property
    def token(self):
        return getattr(self, "_token", None)

    @token.setter
    def token(self, value):
        if self.token == value:
            pass
        elif not isinstance(value, string_types):
            raise TypeError("Auth Token is not of type str.")
        else:
            self._token = value

    def __call__(self, r):
        r.headers["x-auth-token"] = self.token
        return r

class CellCollective(REST):
    _url = "https://cellcollective.org"

    def __init__(self, verbose=False, cache=False):
        self.super = super(CellCollective, self)
        self.super.__init__(name="Cell Collective",
            url=CellCollective._url, verbose=verbose,
            cache=cache)

    def ping(self):
        response = self.http_get("api/ping")
        return response["data"]
    
    @property
    def token(self):
        return getattr(self, "_token", None)

    @token.setter
    def token(self, value):
        if self.token == value:
            pass
        elif not isinstance(value, string_types):
            raise TypeError("Auth Token is not of type str.")
        else:
            self._token = value

    def auth(self, *args, **kwargs):
        token = kwargs.get("token")

        username = kwargs.get("username")
        password = kwargs.get("password")

        params = { }

        if not token:
            if not username:
                raise TypeError("username not provided.")
            if not password:
                raise TypeError("password not provided.")
        
            params = { "username": username, "password": password }
        
            url = self._build_url("_api/login")
            response = self.session.post(url, params=params)

            if response.ok:
                headers = response.headers
                token   = headers.get("x-auth-token")

                if not token:
                    raise CCAuthenticationError("Unable to log into cellcollective using credentials provided.")
                else:
                    self.token = token
            else:
                response.raise_for_status()
        else:
            # TODO: Authentication using token.
            pass

    @property
    def authenticated(self):
        return bool(self.token)

    def _get_default_params(self):
        params = { }
        
        if self.authenticated:
            params["auth"] = CCAuth(token = self.token)
        
        return params

    def get_models(self):
        params = self._get_default_params()
        return self.http_get("_api/model/get", **params)