import requests
from abc import ABC, abstractmethod


class DataFetcher(ABC):
    """A class that handles the retrieval of data from various sources."""

    @abstractmethod
    def fetch(self, source):
        """Fetch data from a specified source.

        This method retrieves data from a given URL or file path. It is essential that the source provided is valid and accessible; otherwise, an exception will be raised.

        Args:
            source (str): The URL or path of the data source to fetch.

        Raises:
            ValueError: If the source is invalid or inaccessible.

        Returns:
            str: The data retrieved from the specified source, if successful.
        """
        pass


class HTTPDataFetcher(DataFetcher):
    """A class that handles the fetching of data over HTTP."""

    def fetch(self, url):
        """Fetch data from a given URL using an HTTP GET request.

        This function sends an HTTP GET request to the specified URL and returns the text content of the response if the request is successful. If an error occurs during the request, it handles the exception and returns None.

        Args:
            url (str): The URL from which to fetch data. It must be a valid URL string.

        Returns:
            str: The text content of the response if the request is successful.
                 Returns None if an error occurs during the request.

        Raises:
            requests.RequestException: If an error occurs during the HTTP request, such as a connection error or a timeout.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None


class FileDataFetcher(DataFetcher):
    """A class that handles the retrieval of file data."""

    def fetch(self, file_path):
        """Read the contents of a file.

        This function attempts to open and read the contents of a specified file. If successful, it returns the contents as a string. If an error occurs during the file reading process, it handles the exception and returns None.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            str: The contents of the file as a string. If an error occurs, None is returned.

        Raises:
            IOError: If an error occurs while reading the file, such as if the file does not exist or is not accessible.
        """
        try:
            with open(file_path, "r") as file:
                return file.read()
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return None


class DataProcessor:
    """A class that processes data retrieved by a fetcher."""

    def __init__(self, fetcher):
        """Initialize the object with a fetcher.

        Args:
            fetcher (object): The fetcher object used to retrieve data.

        Raises:
            None: This constructor does not raise any exceptions.
        """
        self.fetcher = fetcher

    def process(self, source):
        """Process data from a given source.

        This method retrieves data from the specified source and processes it. If data is available, it will be printed and returned; otherwise, a message indicating no data is available will be printed, and None will be returned.

        Args:
            source (str): The data source to process.

        Returns:
            str or None: The data fetched from the source if available; otherwise, None.

        Raises:
            None: This method does not raise any exceptions.
        """
        data = self.fetcher.fetch(source)
        if data:
            print(f"Processing data from {source}")
            return data
        else:
            print(f"No data to process from {source}")
            return None


def main():
    """Fetch and process data from a URL and a file.

    This function fetches data from a specified URL using an instance of `HTTPDataFetcher` and processes it with an instance of `DataProcessor`. Additionally, it fetches data from a specified file using an instance of `FileDataFetcher` and processes it with another instance of `DataProcessor`.

    Returns:
        None: This function does not return any value.

    Raises:
        Exception: Any exceptions raised during the data fetching or processing operations, which may include network-related errors, file I/O errors, or processing errors.
    """
    url = "https://api.github.com"
    file_path = "data.txt"
    http_fetcher = HTTPDataFetcher()
    file_fetcher = FileDataFetcher()
    http_processor = DataProcessor(http_fetcher)
    file_processor = DataProcessor(file_fetcher)
    http_data = http_processor.process(url)
    file_data = file_processor.process(file_path)


if __name__ == "__main__":
    main()
