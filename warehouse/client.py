from databricks import sql
from databricks.sql.client import Connection

from warehouse.credentials.base import BaseDatabricksCredentials

class DatabricksClient:
    def __init__(
        self,
        credentials: BaseDatabricksCredentials
    ):
        self._credentials = credentials
        
    def connection(self) -> Connection:
        return sql.connect(
            server_hostname=self._credentials.server_hostname,
            http_path=self._credentials.http_path,
            access_token=self._credentials.access_token,
        )
        