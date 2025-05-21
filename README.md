# Docstring Generator

A tool to automatically add docstrings to your Python code using various Large Language Models (LLMs) via Langchain, ensuring your code remains unchanged except for the addition of docstrings.

## Features

- **Automatic Docstring Generation**: Generate comprehensive and descriptive docstrings for your Python classes, methods, and functions.
- **Multi-Provider LLM Support**: Utilizes Langchain to integrate with various LLM providers:
  - OpenAI
  - Anthropic
  - Cohere
  - Ollama (for local models)
- **Code Integrity Validation**: Ensures that no changes are made to your code other than adding docstrings.
- **Flexible API Key Management**: Pass your API key via command-line arguments or retrieve it securely from environment variables or Azure Key Vault.
- **Configurable Logging**: Control log verbosity with `--log-level` and `--verbose` options.

## Installation

You can install the `docu-gen` package from PyPI using `pip` (once published):

```bash
pip install docu-gen
```

Alternatively, to install from source (e.g., for development or to get the latest unreleased changes):

1. Clone the repository:

    ```bash
    git clone https://github.com/nadeem4/doc_generator.git
    cd doc_generator/
    ```

2. Install the package:
    - For a standard installation from source (installs runtime dependencies):

        ```bash
        pip install .
        ```

    - For an editable installation (recommended for development), which also installs development tools listed in `requirements.txt` (if `requirements.txt` includes `-e .` and dev dependencies):

        ```bash
        pip install -r requirements.txt
        ```

## Usage

```bash
generate_docstring [options] paths
```

### Positional Arguments

- **paths**: One or more file or directory paths to process. You can specify multiple paths separated by spaces.

### Optional Arguments

- **--exclude**: Patterns to exclude from processing (e.g., '*/test_*', 'venv/*'). Applied to full paths and file names.
  **Example**:

  ```bash
  generate_docstring example_project/ --exclude tests/*
  ```

- **--override**: Overrides existing docstrings. By default, existing docstrings are preserved.
  **Example**:

  ```bash
  generate_docstring example_project/ --override
  ```

- **--provider**: AI provider to use (e.g., `openai`, `anthropic`, `cohere`, `ollama`). Default: `openai`.
  **Example**:

  ```bash
  generate_docstring example_project/ --provider anthropic
  ```

- **--model**: Model name to use for the selected provider. If not provided, a default model for the provider may be used by the LLM client.
  **Example**:

  ```bash
  generate_docstring example_project/ --provider openai --model gpt-4
  ```

- **--api-key**: API key for the selected provider. If provided, it sets the corresponding environment variable (e.g., `OPENAI_API_KEY` for `--provider openai`).
  **Example**:

  ```bash
  generate_docstring example_project/ --provider openai --api-key YOUR_OPENAI_API_KEY
  ```

  If not provided, the program will attempt to retrieve the API key from environment variables or Azure Key Vault.

- **--log-level**: Set the logging level. Choices: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Default: `INFO`.
  **Example**:

  ```bash
  generate_docstring example_project/ --log-level DEBUG
  ```

- **-v, --verbose**: Enable verbose (DEBUG level) logging. Overrides `--log-level`.
  **Example**:

  ```bash
  generate_docstring example_project/ -v
  ```

## API Key Handling

The application retrieves API keys using a chain of responsibility pattern implemented by three handlers:

1. **Command-Line Argument Handler (`--api-key`)**:
    The `CLIAPIKeyHandler` sets the API key in the environment variable if provided via the CLI argument. This is the first handler in the chain and the most direct way to supply a key.

2. **Environment Variable Handler**:
    The `EnvAPIKeyHandler` attempts to retrieve the API key from provider-specific environment variables:
    - For OpenAI: `OPENAI_API_KEY`
    - For Anthropic: `ANTHROPIC_API_KEY`
    - For Cohere: `COHERE_API_KEY`
    - (Ollama typically runs locally and may not require an API key.)

3. **Azure Key Vault Handler**:
    The `AzureKeyVaultAPIKeyHandler` attempts to retrieve the API key from Azure Key Vault if the environment variable is not set. This requires:
    - `AZURE_KEY_VAULT_URL`: The URL of your Azure Key Vault (e.g., `https://your-key-vault-name.vault.azure.net/`).
    - Provider-specific secret name environment variables:
        - For OpenAI: `AZURE_OPENAI_SECRET_NAME` (value should be the name of the secret in Key Vault storing the OpenAI API key).
        - For Anthropic: `AZURE_ANTHROPIC_SECRET_NAME`.
        - For Cohere: `AZURE_COHERE_SECRET_NAME`.
    **Example for Azure Key Vault with OpenAI**:
    Set environment variables:

    ```bash
    export AZURE_KEY_VAULT_URL="https://your-kv.vault.azure.net/"
    export AZURE_OPENAI_SECRET_NAME="MyOpenAISecret"
    ```

    Then run:

    ```bash
    generate_docstring example_project/ --provider openai
    ```

If an API key is required for the selected provider and not found through any of these methods, the program will exit with an error.

## Examples

1. **Generate docstrings for specific files using OpenAI (default provider and model)**:

    ```bash
    # If --provider and --model are omitted, defaults to OpenAI and its default model (e.g., gpt-3.5-turbo).
    generate_docstring module1.py module2.py --api-key YOUR_OPENAI_API_KEY
    ```

2. **Process an entire directory with Anthropic, excluding patterns, with debug logging**:

    ```bash
    generate_docstring example_project/ --provider anthropic --model claude-3-haiku-20240307 --exclude tests/* docs/* --api-key YOUR_ANTHROPIC_API_KEY --log-level DEBUG
    ```

3. **Override existing docstrings using Cohere (e.g., 'command' model) and API key from environment**:
    Assuming `COHERE_API_KEY` is set in your environment:

    ```bash
    generate_docstring example_project/ --provider cohere --model command --override -v
    ```

4. **Use a local Ollama model (e.g., Llama3)**:
    Ensure Ollama is running and the model is pulled (e.g., `ollama pull llama3`).

    ```bash
    generate_docstring example_project/ --provider ollama --model llama3
    ```

5. **Retrieve OpenAI API key from Azure Key Vault**:
    Set environment variables (syntax for Linux/macOS; adapt for Windows, e.g., `set VAR=VALUE` or `$env:VAR="VALUE"`):

    ```bash
    export AZURE_KEY_VAULT_URL="https://your-kv.vault.azure.net/"
    export AZURE_OPENAI_SECRET_NAME="OpenAI-API-Secret"
    ```

    Then run:

    ```bash
    generate_docstring example_project/ --provider openai
    ```

## How It Works

1. **CLI Parsing**: Parses command-line arguments for paths, provider, model, API key, logging, and other options.
2. **Logging Setup**: Initializes the logging system based on `--log-level` or `--verbose` arguments.
3. **API Key Resolution**: The API key for the selected provider is resolved using command-line arguments, environment variables, or Azure Key Vault.
4. **LLM Initialization**: An LLM client is initialized using Langchain with the specified provider, model, and API key.
5. **Docstring Generation**: The tool scans Python files, identifies code elements (classes, functions, methods) needing docstrings (or all if `--override` is used).
6. **Langchain Invocation**: For each item, a request is made to the configured LLM via Langchain to generate a docstring.
7. **Code Integrity Validation**: Ensures that only docstrings were added and no other code changes occurred.
8. **File Update**: The modified code with new docstrings is written back to the file.

## Requirements

- Python 3.8 or higher (due to Langchain dependencies)
- Langchain and provider-specific libraries (e.g., `langchain-openai`, `langchain-anthropic`). These are installed as dependencies.
- API key for the chosen cloud LLM provider (OpenAI, Anthropic, Cohere).
- Azure credentials (if using Azure Key Vault).
- Ollama installed and running with desired models pulled (if using Ollama).

## LLM Integration

The tool leverages Langchain to interface with various LLMs. This allows flexibility in choosing the model and provider that best suits your needs. Ensure you have the necessary API keys and permissions for the cloud providers you intend to use. For local models with Ollama, ensure your Ollama service is operational.

## Security Notes

- **API Keys**: Be cautious with your API keys. Do not hard-code them into your scripts or share them publicly. Use environment variables or a secrets manager like Azure Key Vault.
- **Azure Authentication**: When using Azure Key Vault, the `DefaultAzureCredential` attempts multiple authentication methods. Ensure your environment is set up for one of the supported authentication methods (e.g., Azure CLI, Environment Variables, Managed Identity).

## License

This project is licensed under the MIT License.
