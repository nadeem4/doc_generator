from setuptools import setup, find_packages

setup(
    name="docu-gen",
    version="1.0.6",
    description="A tool to add docstrings to Python code using LLMs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nadeem Khan",
    author_email="nadeem4.nk13@gmail.com",
    url="https://github.com/nadeem4/doc_generator",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "astor>=0.8.1,<0.9.0",
        "libcst>=1.4.0,<2.0.0",
        "openai>=1.52.1,<2.0.0",
        "azure-identity>=1.7.0,<2.0.0",
        "azure-keyvault-secrets>=4.2.0,<5.0.0",
        "azure-storage-blob>=12.8.0,<13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "generate_docstring=docu_gen.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
