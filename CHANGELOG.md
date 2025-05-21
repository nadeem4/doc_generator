# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.8.0] - 2024-06-01

### Added
- Implemented `CLIAPIKeyHandler` to handle API key retrieval from CLI arguments.
- Enhanced API key management with a proper chain of responsibility pattern across CLI, environment variables, and Azure Key Vault.
- Updated `LLM` class to use the new API key handler chain for robust key resolution.
- Added logging for API key handler operations and LLM initialization.
- Added `--log-level` and `--verbose` CLI options for configurable logging verbosity.

### Changed
- Refactored API key handlers (`EnvAPIKeyHandler`, `AzureKeyVaultAPIKeyHandler`) to implement the `handle` method and delegate to successors.
- Updated `llm.py` to fix API key resolution logic and imports.
- Updated `README.md` to document the new API key handler chain and logging options.

### Fixed
- Fixed missing `handle` method implementations in API key handler subclasses.
- Fixed incorrect method calls (`handle_request` to `handle`) in `llm.py`.

## [1.7.0] - Previous Release

- Previous changelog entries...
