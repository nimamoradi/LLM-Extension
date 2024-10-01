from abc import ABC, abstractmethod
import time

class ExtensionBase(ABC):
    TIMEOUT = 5  # Timeout in seconds, can be adjusted or overridden

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
        try:
            start_time = time.time()
            result = self.process(query)
            elapsed_time = time.time() - start_time
            if elapsed_time > self.TIMEOUT:
                raise TimeoutError(f"Extension timed out after {self.TIMEOUT} seconds")
            return result
        except Exception as e:
            return f"An error occurred: {str(e)}"
