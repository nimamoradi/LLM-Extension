import uuid
import ollama
from dataclasses import dataclass


class OllamaConnector:
    def __init__(self):
        self.client = ollama.Client()
        self.modelName = 'llama3:latest'
        self.conversation_history = []

    def start_conversation(self, message: str):
        id = self._create_id()
        # add to conversation history
        self.conversation_history.append({
            'id': id,
            'role': 'user',
            'content': message,
        })
        response = self._chat([{
            'id': id,
            'role': 'user',
            'content': message,
        }, ], id)
        return response['message']['content'], id

    def _chat(self, messages: list, id: str):
        # this is a private method to chat with ollama
        # both start_conversation and follow_up will call this method
        response = self.client.chat(model=self.modelName, messages=messages)
        # add responseto conversation history
        self.conversation_history.append({
            'id': id,
            'role': 'assistant',
            'content': response['message']['content'],
        })
        return response

    # follow-up will keep the responses in memory and use it to generate the next response
    # it will also keep the conversation history
    # and use it to generate the next response as system prompt given the conversation history
    def follow_up(self, id: str, message: str):
        # pull old messages for id
        old_messages = [message for message in self.conversation_history if message['id'] == id]
        # add new messages

        old_messages.append({
            'id': id,
            'role': 'user',
            'content': message,
        })
        self.conversation_history.append({
            'id': id,
            'role': 'user',
            'content': message,
        })
        # generate response
        response = self._chat(old_messages, id)
        return response['message']['content']

    # remove all conversations from memory
    def clear_all(self):
        self.conversation_history = []

    # remove a specific conversation from memory
    def clear_conversation(self, id: str):
        self.conversation_history = [message for message in self.conversation_history if message.id != id]

    def _create_id(self):
        return str(uuid.uuid4())
