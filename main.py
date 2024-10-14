from src.Extensions.WeatherExtension import WeatherExtension
from src.ExtensionController import ExtensionController
from src.OllamaConnector import OllamaConnector

if __name__ == '__main__':
    # Example OllamaConnector usage
    ollama = OllamaConnector()

    # Create an extension controller and add extensions
    controller = ExtensionController(ollama)
    controller.add_extension(WeatherExtension(ollama))  # Add your extensions here

    conversation_id = None  # Initialize conversation ID

    print("Welcome to the LLM Assistant. Type 'exit' to quit.")

    while True:
        # Get user input from the terminal
        user_input = input("\nYou: ")

        # Check if the user wants to exit the app
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        # Handle the query using the assistant controller
        response, conversation_id = controller.handle_query(user_input, conversation_id)

        # Display the response
        print(f"Assistant: {response}")
