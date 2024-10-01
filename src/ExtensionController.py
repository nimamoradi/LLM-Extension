import ExtensionBase


class ExtensionController:
    def __init__(self):
        self.extensions = []
    
    def add_extension(self, extension: ExtensionBase):
        self.extensions.append(extension)

    def handle_query(self, query: str) -> str:
        for extension in self.extensions:
            if extension.matches(query):
                return extension.execute(query)
        return self.fallback_response(query)

    def fallback_response(self, query: str) -> str:
        # Fallback response if no extension matches the query
        return "I'm sorry, I don't understand your request."
