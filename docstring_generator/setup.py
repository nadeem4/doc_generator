from setuptools import setup, find_packages

setup(
    name="docstring_adder",
    version="1.0.0",
    description="A tool to add docstrings to Python code using LLMs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nadeem Khan",
    author_email="nadeem4.nk13@gmail.com",
    url="https://github.com/nadeem4/doc_generator",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "libcst>=0.3.19",
        # Add any other dependencies your project requires
    ],
    entry_points={
        "console_scripts": [
            "generate_docstring=docstring_generator.cli:main",
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
