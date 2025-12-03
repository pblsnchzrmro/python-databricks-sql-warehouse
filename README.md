# Databricks SQL Warehouse Client

A Python client library for connecting to Databricks SQL Warehouse with support for multiple authentication methods.

## Features

- **PAT Authentication**: Connect using Personal Access Tokens
- **OAuth Authentication**: Connect using OAuth client credentials
- **Azure Key Vault Integration**: Securely retrieve credentials from Azure Key Vault
- **Simple Configuration**: JSON-based configuration files

## Installation

```bash
pip install databricks-sql-connector azure-identity azure-keyvault-secrets
```

## Usage

### 1. PAT Authentication

```bash
# Copy and configure
cp config_pat.example.json config_pat.json
# Edit config_pat.json with your credentials
python main_pat.py
```

### 2. OAuth Authentication

```bash
# Copy and configure
cp config_oauth.example.json config_oauth.json
# Edit config_oauth.json with your credentials
python main_oauth.py
```

### 3. Azure Key Vault

```bash
# Copy and configure
cp config_keyvault.example.json config_keyvault.json
# Edit config_keyvault.json with your Key Vault URL
python main_keyvault.py
```

## Configuration Files

All configuration files are gitignored for security. Use the `.example.json` templates to create your own configuration files.
