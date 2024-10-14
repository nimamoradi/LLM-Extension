# LLaMA 3 Assistant with Custom Extensions
Introduction
This project demonstrates how easily custom extensions can be integrated into LLaMA 3 or any other language model (LLM) using a simple mechanism. The goal is to enable the model to handle specific tasks like generating text, performing operations, or fetching data, without relying solely on the LLM for everything. For simplicity, a weather forecast extension is included as an example.

## Extensions Framework
Defining an Extension
Each extension inherits from the ExtensionBase class, which provides a clear structure for implementing new functionalities. The abstract class outlines the core methods that every extension needs to define.

```python
from abc import ABC, abstractmethod
import time

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
```
## Creating an Extension
For example, the WeatherExtension detects weather-related queries and processes them by fetching the weather forecast.

```python
class WeatherExtension(ExtensionBase):
    def matches(self, query: str) -> bool:
        return "weather" in query.lower()

    def process(self, query: str) -> str:
        # Fetch weather data based on the query
        return f"Weather forecast for {query}"
```
## Registering Extensions
To use the defined extensions, they need to be registered with the ExtensionController, which checks each query to see if any of the available extensions can handle it.

Here’s how you can register an extension:

```python
# Registering Extensions
controller = ExtensionController(ollama)
controller.add_extension(WeatherExtension(ollama))
```
The ExtensionController iterates through all registered extensions and delegates the query processing to the first extension that matches the query.

```python
class ExtensionController:
    def __init__(self, llm_connector: OllamaConnector):
        self.extensions = []
        self.ollama = llm_connector
    
    def add_extension(self, extension: ExtensionBase):
        self.extensions.append(extension)

    def handle_query(self, query: str, conversation_id: str = None) -> str:
        for extension in self.extensions:
            if extension.matches(query):
                response = extension.execute(query)
                return self.ollama.follow_up(conversation_id, response)
        return self.ollama.start_conversation(query)
```
## How to Run
Clone the repository.
Set up your environment with the required dependencies (Python, Ollama).
Add your own extensions or use the existing ones like the weather forecast.
Run the terminal app to interact with the LLM using the extensions.
Example Usage
In the terminal, you can input queries like:

```shell
You: What's the weather in New York tomorrow?
Assistant: The weather forecast for New York tomorrow is...
```
## Future Work
here are the things that can be done, not in-order 
* Add integration for Gemini and OpenAI and Claude LLM
* Add more extension like math or map, code runners
* Make extension able to handle follow-ups