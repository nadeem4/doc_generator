
# Docstring Generator

A tool to automatically add docstrings to your Python code using Large Language Models (LLMs), ensuring your code remains unchanged except for the addition of docstrings.

## Features

- **Automatic Docstring Generation**: Generate comprehensive and descriptive docstrings for your Python classes, methods, and functions.
- **OpenAI Integration**: Utilize OpenAI's powerful language models to create meaningful docstrings.
- **Code Integrity Validation**: Ensures that no changes are made to your code other than adding docstrings.
- **Flexible API Key Management**: Pass your OpenAI API key via command-line arguments or retrieve it securely from Azure Key Vault.

## Installation

You can install the `docstring_generator` package using `pip`:

```bash
pip install docstring_generator
```

Alternatively, clone the repository and install the required packages:

```bash
git clone https://github.com/nadeem4/doc_generator.git
cd doc_generator/docstring_generator
pip install .
```

## Usage

```bash
generate_docstring [options] paths
```

### Positional Arguments

- **paths**: One or more file or directory paths to process. You can specify multiple paths separated by spaces.

### Optional Arguments

- **--exclude**: Patterns to exclude from processing. Accepts multiple patterns.

  **Example**:

  ```bash
  generate_docstring example_project/ --exclude tests/* 
  ```

  This command processes all files in `example_project/` except those in `tests/` directories.

- **--override**: Overrides existing docstrings. By default, existing docstrings are preserved.

  **Example**:

  ```bash
  generate_docstring example_project/ --override
  ```

  This command regenerates docstrings even if they already exist in the code.

- **--apikey**: Your OpenAI API key.

  **Example**:

  ```bash
  generate_docstring example_project/ --apikey YOUR_OPENAI_API_KEY
  ```

  If not provided, the program will attempt to retrieve the API key from environment variables or Azure Key Vault.

## API Key Handling

The application retrieves the OpenAI API key using a chain of responsibility pattern with the following handlers:

1. **Command-Line Argument**: If the `--apikey` argument is provided, it uses this value.

2. **Environment Variable**: Checks for the `OPENAI_API_KEY` environment variable.

   ```bash
   generate_docstring example_project/
   ```

3. **Azure Key Vault**: Retrieves the API key from Azure Key Vault using `AZURE_KEY_VAULT_URL` and `AZURE_SECRET_NAME` environment variables.

   ```bash
   generate_docstring example_project/
   ```

If the API key is not found through any of these methods, the program will exit with an error message.

## Examples

1. **Generate docstrings for specific files**:

   ```bash
   generate_docstring module1.py module2.py
   ```

2. **Process an entire directory excluding certain patterns**:

   ```bash
   generate_docstring example_project/ --exclude tests/* docs/*
   ```

3. **Override existing docstrings and provide API key via command-line**:

   ```bash
   generate_docstring example_project/ --override --apikey YOUR_OPENAI_API_KEY
   ```

4. **Retrieve API key from Azure Key Vault**:

   Set the necessary environment variables:

   ```bash
   AZURE_KEY_VAULT_URL=https://your-key-vault-name.vault.azure.net/
   AZURE_SECRET_NAME=OpenAIAPIKey
   ```

   Then run:

   ```bash
   generate_docstring example_project/
   ```

## Explanation of Arguments

- **paths**: Specifies the files or directories to process. Multiple paths can be provided.

- **--exclude**: Patterns to exclude from processing. Useful for skipping directories like tests or documentation. Accepts glob patterns.

- **--override**: If set, the tool will overwrite existing docstrings. By default, it only adds docstrings where they are missing.

- **--apikey**: Your OpenAI API key. If not provided, the tool looks for the API key in the environment variables or Azure Key Vault.

## How It Works

1. **Docstring Generation**: The tool scans the specified Python files and identifies functions, classes, and methods lacking docstrings.

2. **OpenAI API Call**: For each item needing a docstring, the tool sends a request to the OpenAI API to generate an appropriate docstring.

3. **Code Integrity Validation**: After generating the docstrings, the tool checks to ensure that only docstrings were added and no other code changes occurred.

4. **API Key Retrieval**: Utilizes a handler chain to securely retrieve the OpenAI API key from the command-line argument, environment variable, or Azure Key Vault.

## Requirements

- Python 3.6 or higher
- An OpenAI API key
- Azure credentials (if using Azure Key Vault)

## OpenAI Integration

Ensure you have access to the OpenAI API and have sufficient credits or a subscription plan. The tool uses the API to generate human-like docstrings based on your code.


## Security Notes

- **API Keys**: Be cautious with your API keys. Do not hard-code them into your scripts or share them publicly.
- **Azure Authentication**: When using Azure Key Vault, the `DefaultAzureCredential` attempts multiple authentication methods. Ensure your environment is set up for one of the supported authentication methods (e.g., Azure CLI, Environment Variables, Managed Identity).

## License

This project is licensed under the MIT License.
