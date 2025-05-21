# Contributing to Docu-Gen

First off, thank you for considering contributing to Docu-Gen! It's people like you that make Docu-Gen such a great tool.

## Where do I go from here?

If you've noticed a bug or have a feature request, [make one](https://github.com/nadeem4/doc_generator/issues/new)! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

If you have a general question, feel free to ask in the [Discussions](https://github.com/nadeem4/doc_generator/discussions) section.

## Fork &amp; create a branch

If you're ready to contribute code, fork the repository and create a new branch from `main` for your changes. A good branch name would be descriptive of the change you're making (e.g., `fix-parsing-error` or `add-new-llm-provider`).

## Setting up the Development Environment

This project uses [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) to provide a consistent and ready-to-use development environment.

**Prerequisites:**
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/)
*   [Visual Studio Code](https://code.visualstudio.com/)
*   [VS Code Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

**Steps:**

1.  **Clone your fork:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/doc_generator.git
    cd doc_generator
    ```

2.  **Open in Dev Container:**
    *   Open the cloned `doc_generator` folder in VS Code.
    *   VS Code should automatically detect the `.devcontainer/devcontainer.json` file and prompt you to "Reopen in Container". Click it.
    *   If not prompted, open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P) and search for "Dev Containers: Reopen in Container" or "Dev Containers: Open Folder in Container...".

    This will build and start the dev container. The `postCreateCommand` in `devcontainer.json` will automatically:
    *   Install all dependencies from `requirements.txt` (including the package in editable mode).
    *   Install `pre-commit` hooks.

    You are now ready to code! `black` and `docformatter` (and any other configured pre-commit hooks) will run automatically before each commit.

### Alternative: Manual Setup (if not using Dev Containers)

If you prefer not to use Dev Containers, you can set up your environment manually:

1.  **Clone your fork** (as above).

2.  **Create a virtual environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    Install the package in editable mode along with development dependencies.
    ```bash
    pip install -r requirements.txt
    pip install -e .
    ```

4.  **Set up pre-commit hooks:**
    This project uses `pre-commit` to ensure code quality and consistency.
    ```bash
    pre-commit install
    ```


## Making Changes

*   Write clean, readable code with clear comments where necessary.
*   Ensure your code follows the existing style of the project.
*   Add tests for any new features or bug fixes. Ensure all tests pass by running `pytest`.
*   Update documentation (README.md, docstrings, etc.) if your changes affect usage or functionality.
*   Make sure your changes don't break existing functionality.

## Running Tests

To run the test suite:
```bash
pytest
```
To run tests with coverage:
```bash
pytest --cov=docu_gen
```

## Submitting your contribution

Once your changes are ready, make sure all pre-commit hooks pass and all tests pass. Then, push your branch to your fork and [submit a pull request](https://github.com/nadeem4/doc_generator/compare) to the `main` branch of the original repository.

In your pull request description, please explain the changes you've made and why. If your PR addresses an existing issue, please link to it.

## Code of Conduct

By contributing to Docu-Gen, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

Thank you for your contribution!
