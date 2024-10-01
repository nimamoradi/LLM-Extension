from src.OllamaConnector import OllamaConnector


# The ollama connector test

# Test 1 check if it can start a conversation


def test_start_conversation():
    ollama = OllamaConnector()
    response, id = ollama.start_conversation('Hello, how are you?')
    assert response is not None
    assert response != ''
    print(response)


# Test 2 check if it can follow up a conversation
# tell it somthing and check it can recall it in the next message
def test_follow_up_conversation():
    ollama = OllamaConnector()
    response, id = ollama.start_conversation('Hello, I am John remember my name.')
    assert response is not None
    assert response != ''
    print(response)
    response = ollama.follow_up(id, 'what was my name?')
    assert response is not None
    assert response != ''
    print(response)

