from abc import ABC, abstractmethod
import time

from src import OllamaConnector


class ExtensionBase(ABC):
    def __init__(self, llm: OllamaConnector):
        self.llm = llm
        self.TIMEOUT = 10  # Timeout in seconds, can be adjusted or overridden

    @abstractmethod
    def matches(self, query: str) -> bool:
        """Check if this extension can handle the query."""
        pass

    @abstractmethod
    def process(self, query: str) -> str:
        """Process the query and return a result."""
        pass

    def execute(self, query: str) -> str:
        """Execute the extension with timeout handling."""
        start_time = time.time()
        result = self.process(query)
        return result
