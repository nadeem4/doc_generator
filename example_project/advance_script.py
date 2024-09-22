import requests
from abc import ABC, abstractmethod

class DataFetcher(ABC):
    """Abstract base class for data fetchers."""

    @abstractmethod
    def fetch(self, source):
        """Fetch data from a source."""
        pass

class HTTPDataFetcher(DataFetcher):
    """Fetch data over HTTP."""

    def fetch(self, url):
        """Fetch data from a URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None

class FileDataFetcher(DataFetcher):
    """Fetch data from a local file."""

    def fetch(self, file_path):
        """Fetch data from a file."""
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return None

class DataProcessor:
    """Process data fetched from a source."""

    def __init__(self, fetcher):
        self.fetcher = fetcher

    def process(self, source):
        """Fetch and process data from the source."""
        data = self.fetcher.fetch(source)
        if data:
            print(f"Processing data from {source}")
            # Add processing logic here
            return data
        else:
            print(f"No data to process from {source}")
            return None

def main():
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
