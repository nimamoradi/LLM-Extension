
class ExtensionController:
    def __init__(self, ollama_connector):
        self.extensions = []
        self.ollama = ollama_connector  # OllamaConnector instance

    def add_extension(self, extension):
        self.extensions.append(extension)

    def handle_query(self, query: str, conversation_id: str = None) -> str:
        # Check extensions first
        for extension in self.extensions:
            if extension.matches(query):
                response = extension.execute(query)
                # If there's no conversation ID, start a new conversation using extension response
                if conversation_id is None:
                    response, conversation_id = self.ollama.start_conversation(response)
                else:
                    response = self.ollama.follow_up(conversation_id, response)
                return response, conversation_id

        # If no extension matches, use the LLM directly
        if conversation_id:
            return self.ollama.follow_up(conversation_id, query)
        else:
            response, conversation_id = self.ollama.start_conversation(query)
            return response, conversation_id