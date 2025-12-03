"""
Connect to Databricks SQL Warehouse using OAuth authentication.
Configuration is loaded from config_oauth.json file.
"""
import json
import sys
from pathlib import Path
from warehouse.credentials.base import DatabricksOAuthStaticCredentials
from warehouse.client import DatabricksClient


def load_config(config_path: str = "config_oauth.json") -> dict:
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
        print("Please create it based on 'config_oauth.example.json'")
        sys.exit(1)
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)


def main():
    """Main entry point for OAuth authentication."""
    print("Connecting to Databricks using OAuth authentication...")
    
    config = load_config()
    databricks_config = config.get("databricks", {})
    
    creds = DatabricksOAuthStaticCredentials(
        server_hostname=databricks_config.get("server_hostname"),
        http_path=databricks_config.get("http_path"),
        client_id=databricks_config.get("client_id"),
        client_secret=databricks_config.get("client_secret")
    )

    client = DatabricksClient(credentials=creds)

    try:
        with client.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_user()")
            rows = cursor.fetchall()
            
        print(f"✓ Connection successful. Current user: {rows}")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
