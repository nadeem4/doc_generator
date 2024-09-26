import requests
from abc import ABC, abstractmethod


class DataFetcher(ABC):
    """A class for fetching data from various sources."""

    @abstractmethod
    def fetch(self, source):
        """
Fetch data from a specified source.

Args:
    source (str): The URL or path of the data source to fetch.

Raises:
    ValueError: If the source is invalid or inaccessible.
"""
        pass


class HTTPDataFetcher(DataFetcher):
    """A class for fetching HTTP data."""

    def fetch(self, url):
        """
Fetch data from a given URL using an HTTP GET request.

Args:
    url (str): The URL from which to fetch the data.

Returns:
    str: The text content of the response if the request is successful.

Raises:
    requests.RequestException: If an error occurs during the HTTP request.
"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f'Error fetching data from {url}: {e}')
            return None


class FileDataFetcher(DataFetcher):
    """A class for fetching data from files."""

    def fetch(self, file_path):
        """
Read the content of a file.

Args:
    file_path (str): The path to the file to be read.

Returns:
    str: The content of the file as a string.

Raises:
    IOError: If an error occurs while reading the file.
"""
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except IOError as e:
            print(f'Error reading file {file_path}: {e}')
            return None


class DataProcessor:
    """A class for processing data."""

    def __init__(self, fetcher):
        """
Initialize a new instance of the class.

Args:
    fetcher (object): An object used for fetching data.

Raises:
    None
"""
        self.fetcher = fetcher

    def process(self, source):
        """
Process data from a given source.

Args:
    source (str): The data source to process.

Returns:
    str or None: The data fetched from the source if available, otherwise None.

Raises:
    None.
"""
        data = self.fetcher.fetch(source)
        if data:
            print(f'Processing data from {source}')
            return data
        else:
            print(f'No data to process from {source}')
            return None


def main():
    """
Fetch and process data from a URL and a file.

Fetches data from a given URL and a file path using HTTPDataFetcher and FileDataFetcher respectively.
Processes the fetched data using DataProcessor for both HTTP and file data.

Returns:
    None

Raises:
    Any exceptions raised during data fetching or processing.
"""
    url = 'https://api.github.com'
    file_path = 'data.txt'
    http_fetcher = HTTPDataFetcher()
    file_fetcher = FileDataFetcher()
    http_processor = DataProcessor(http_fetcher)
    file_processor = DataProcessor(file_fetcher)
    http_data = http_processor.process(url)
    file_data = file_processor.process(file_path)


if __name__ == '__main__':
    main()
