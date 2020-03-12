from bioservices.services import REST, BioServicesError

__all__ = ["CellCollective"]

class CCAuthenticationError(BioServicesError):
    pass

class CellCollective(REST):
    _url = "https://cellcollective.org"

    def __init__(self, verbose=False, cache=False):
        self.super = super(CellCollective, self)
        self.super.__init__(name="Cell Collective",
            url=CellCollective._url, verbose=verbose,
            cache=cache)

    def ping(self):
        return self.http_get("api/ping")

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
        else:
            pass

        params = params
        response = self.session.get("_api/login", params=params)

        if response.ok:
            pass
        else:
            raise CCAuthenticationError("Unable to log in into cellcollective.")