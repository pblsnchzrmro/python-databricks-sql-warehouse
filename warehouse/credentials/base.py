import abc
import requests

from functools import cached_property

# property es para exponer datos como si fuesen propiedades, como todo lo que se ve aqui

class BaseDatabricksCredentials(abc.ABC):
    @property
    @abc.abstractmethod
    def server_hostname(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def http_path(self) -> str:
        pass
    
    @property
    @abc.abstractmethod
    def access_token(self) -> str:
        pass
    
    
class BaseDatabricksOAuthCredentials(BaseDatabricksCredentials):
    @property
    @abc.abstractmethod
    def client_id(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def client_secret(self) -> str:
        pass

    @cached_property
    def access_token(self) -> str: # type: ignore[override]
        token_url = f"https://{self.server_hostname}/oidc/v1/token"
        resp = requests.post(
            token_url,
            auth=(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials", "scope": "all-apis"},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["access_token"]
    
class BaseDatabricksTokenCredentials(BaseDatabricksCredentials):
    @property
    @abc.abstractmethod
    def access_token(self) -> str:
        pass
    
class DatabricksPATWarehouseCredentials(BaseDatabricksTokenCredentials):
    def __init__(self, server_hostname: str, http_path: str, access_token: str):
        self._server_hostname = server_hostname
        self._http_path = http_path
        self._access_token = access_token

    @property
    def server_hostname(self) -> str:
        return self._server_hostname

    @property
    def http_path(self) -> str:
        return self._http_path

    @property
    def access_token(self) -> str:
        return self._access_token

class DatabricksOAuthStaticCredentials(BaseDatabricksOAuthCredentials):
    def __init__(self, server_hostname, http_path, client_id, client_secret):
        self._server_hostname = server_hostname
        self._http_path = http_path
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def server_hostname(self):
        return self._server_hostname

    @property
    def http_path(self):
        return self._http_path

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret
