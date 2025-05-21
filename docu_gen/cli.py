"""Command-line interface for the docstring generator."""

import argparse
import logging
import os
import sys
import fnmatch # Ensure fnmatch is imported
from typing import List, Optional

from docu_gen.core.docstring_adder import add_docstrings_to_file
from docu_gen.utils.logging_config import setup_logging
# Assuming AI_MODEL constant might be used for default model if not provided
# from docu_gen.core.constant import AI_MODEL

# Get a logger instance for this module
logger = logging.getLogger("docu_gen")

def set_api_key_env_from_cli(provider: Optional[str], api_key: Optional[str]) -> None:
    """
    Sets the appropriate environment variable for the given provider's API key
    if the API key is provided via the --api-key CLI argument.

    Args:
        provider: The AI provider (e.g., 'openai', 'anthropic', 'cohere').
        api_key: The API key string.
    """
    if not api_key: # Do nothing if no API key is provided via CLI
        return

    if not provider:
        logger.warning(
            "An API key was provided via --api-key, but no --provider was specified. "
            "The API key cannot be set in the environment without knowing the provider."
        )
        return

    provider_upper = provider.upper()
    env_var_name = f"{provider_upper}_API_KEY"
    
    # Specific handling for Azure OpenAI as it might use a different pattern
    # or be handled by azure-identity. For now, assume direct key if provider is 'azure'.
    # if provider.lower() == "azure":
    #     env_var_name = "AZURE_OPENAI_API_KEY" # Or relevant Azure SDK variable

    os.environ[env_var_name] = api_key
    logger.info(f"API key for {provider} set in environment variable {env_var_name} from --api-key argument.")


def process_paths(paths: List[str], exclude: Optional[List[str]], override: bool,
                 provider: str, model: Optional[str], api_key: Optional[str]) -> None:
    """Process the given paths to add docstrings.

    Args:
        paths: List of file or directory paths to process.
        exclude: List of patterns to exclude.
        override: Whether to override existing docstrings.
        provider: The AI provider to use.
        model: The model name to use.
        api_key: The API key for the provider (from CLI).
    """
    # Set API key in environment if provided via CLI
    # This allows the ApikeyHandler chain to pick it up if it checks env vars first for the given provider
    set_api_key_env_from_cli(provider, api_key)

    # Default model logic (example, adjust as per actual default model strategy)
    # actual_model = model
    # if not actual_model:
    #     if provider == AI_MODEL.get("provider"): # Check if provider matches the one in constant
    #         actual_model = AI_MODEL.get("model_name")
    #     else:
    #         # Here you might want to have a dictionary of default models per provider
    #         # or raise an error if model is not specified for non-default provider
    #         logger.warning(f"No model specified for provider '{provider}'. LLM may use its default or fail.")
    # else:
    #    logger.info(f"Using model '{actual_model}' for provider '{provider}'.")


    for path_arg in paths:
        if os.path.isfile(path_arg):
            if path_arg.endswith('.py'):
                logger.debug(f"Processing single file: {path_arg}")
                add_docstrings_to_file(path_arg, override=override, provider=provider, model_name=model)
            else:
                logger.info(f"Skipping non-Python file: {path_arg}")
        elif os.path.isdir(path_arg):
            logger.debug(f"Processing directory: {path_arg}")
            for root, _, files in os.walk(path_arg):
                for file in files:
                    if not file.endswith('.py'):
                        continue
                    
                    file_path = os.path.join(root, file)
                    
                    # Exclusion logic
                    excluded = False
                    if exclude:
                        for pattern in exclude:
                            if fnmatch.fnmatch(os.path.abspath(file_path), os.path.abspath(pattern)) or \
                               fnmatch.fnmatch(file, pattern): # Check file name and full path
                                logger.info(f"Excluding file due to pattern '{pattern}': {file_path}")
                                excluded = True
                                break
                    if excluded:
                        continue
                    
                    add_docstrings_to_file(file_path, override=override, provider=provider, model_name=model)
        else:
            logger.warning(f"Path does not exist or is not a file/directory: {path_arg}")

def main():
    """Main entry point for the docstring generator CLI."""
    parser = argparse.ArgumentParser(
        description="Add docstrings to Python code using LLMs."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more file or directory paths to process.",
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        help="Patterns to exclude from processing (e.g., '*/test_*', 'venv/*'). Applied to full paths and file names.",
    )
    parser.add_argument(
        "--override",
        action="store_true",
        help="Override existing docstrings.",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="openai", # Default provider
        help="AI provider to use (e.g., openai, anthropic, cohere, ollama). Default: openai.",
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Model name to use for the selected provider. If not provided, a default model for the provider may be used by the LLM client.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key for the selected provider. If provided, it sets the corresponding environment variable (e.g., OPENAI_API_KEY).",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level. Default: INFO.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (DEBUG level) logging. Overrides --log-level.",
    )

    args = parser.parse_args()
    
    # Set up logging
    setup_logging(level=args.log_level, verbose=args.verbose)
    
    logger.debug(f"CLI arguments: {args}")

    try:
        process_paths(
            args.paths,
            args.exclude,
            args.override,
            args.provider,
            args.model,
            args.api_key, # Pass CLI API key to process_paths
        )
        logger.info("Docstring generation process completed.")
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user.")
        sys.exit(130) # Standard exit code for Ctrl+C
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True) # exc_info=True logs stack trace
        sys.exit(1)

if __name__ == "__main__":
    main()
