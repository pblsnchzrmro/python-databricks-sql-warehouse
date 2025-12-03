"""
Main script to connect to Databricks SQL Warehouse using Azure Key Vault credentials.
Configuration is loaded from config_keyvault.json file.
"""
import json
import sys
from pathlib import Path
from warehouse.credentials.azure import DatabricksWarehouseCredentialsAzure
from warehouse.client import DatabricksClient


def load_config(config_path: str = "config_keyvault.json") -> dict:
    """
    Load configuration from JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is not valid JSON
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        print(f"Error: Configuration file '{config_path}' not found.")
        print("Please create it based on 'config_keyvault.example.json'")
        sys.exit(1)
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)


def test_keyvault_connection(config: dict) -> None:
    """
    Test connection using Azure Key Vault credentials.
    
    Args:
        config: Configuration dictionary containing Azure Key Vault settings
    """
    print("Testing Azure Key Vault authentication...")
    
    azure_config = config.get("azure", {})
    keyvault_url = azure_config.get("keyvault_url")
    
    if not keyvault_url:
        print("Error: keyvault_url not found in configuration")
        sys.exit(1)
    
    creds = DatabricksWarehouseCredentialsAzure(
        keyvault_url=keyvault_url
    )

    client = DatabricksClient(credentials=creds)

    try:
        with client.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_user()")
            rows = cursor.fetchall()
            
        print(f"✓ Azure Key Vault connection successful. Current user: {rows}")
    except Exception as e:
        print(f"✗ Azure Key Vault connection failed: {e}")


def main():
    """Main entry point for the script."""
    config = load_config()
    test_keyvault_connection(config)


if __name__ == "__main__":
    main()
