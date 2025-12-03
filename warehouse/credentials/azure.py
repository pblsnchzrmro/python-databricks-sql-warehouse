import os
from functools import cached_property
from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from warehouse.credentials.base import BaseDatabricksOAuthCredentials


class DatabricksWarehouseCredentialsAzure(BaseDatabricksOAuthCredentials):
    def __init__(
        self,
        keyvault_url: Optional[str] = None,
        client_id_secret_name: str = "databricks-sql-warehouse-client-id",
        client_secret_secret_name: str = "databricks-sql-warehouse-server-client-secret",
        server_hostname_secret_name: str = "databricks-sql-warehouse-server-hostname",
        http_path_secret_name: str = "databricks-sql-warehouse-http-path",
        credential=None,
    ):
        """
        Retrieve Databricks SQL Warehouse credentials from Azure Key Vault.
        """
        # Key Vault URL puede venir del parámetro o variable de entorno
        self._keyvault_url = keyvault_url or os.environ.get("AZURE_KEYVAULT_URL")
        if not self._keyvault_url:
            raise ValueError("Key Vault URL required (argument or AZURE_KEYVAULT_URL).")

        self._client_id_secret_name = client_id_secret_name
        self._client_secret_secret_name = client_secret_secret_name
        self._server_hostname_secret_name = server_hostname_secret_name
        self._http_path_secret_name = http_path_secret_name

        # Credential de Azure (Managed Identity, CLI, VS Code, etc.)
        self._credential = credential or DefaultAzureCredential()

    @cached_property
    def secrets_client(self) -> SecretClient: 
        return SecretClient(vault_url=self._keyvault_url, credential=self._credential) # type: ignore[arg-type]

    def _get_secret(self, name: str) -> str:
        return self.secrets_client.get_secret(name).value # type: ignore[arg-type]

    @property
    def client_id(self) -> str:
        return self._get_secret(self._client_id_secret_name)

    @property
    def client_secret(self) -> str:
        return self._get_secret(self._client_secret_secret_name)

    @property
    def server_hostname(self) -> str:
        return self._get_secret(self._server_hostname_secret_name)

    @property
    def http_path(self) -> str:
        return self._get_secret(self._http_path_secret_name)
