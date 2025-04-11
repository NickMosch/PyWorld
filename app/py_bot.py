import random

responses={
    "hello": ["Hello there, I'm PyBot!", "Hi! How can I help you today?","How can i assist you today?"],
    "how are you": ["I'm just a bunch of code, but I'm doing fine!", "I'm good, thanks for asking!"],
    "bye": ["Goodbye, fellow programmer!", "Talk to you later!", "Bye! Have a great day!"],
    "name": ["My name is PyBot! Nice to meet you."],
    "default": ["I'm not sure how to respond to that.", "Could you ask me something else?"]
}
def preprocess(text):
    return text.lower()

def get_response(user_input):
    user_input = preprocess(user_input)
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return random.choice(responses["default"])

def chat():
    print("\nPyBot: Greetings, fellow Python!\nI am here to assist you in navigating PyWorld. Type 'bye' to exit.")
    while True:
        user_input=input("You: ")
        if "bye" in user_input.lower():
            print("PyBot:", random.choice(responses["bye"]))
            break
        response = get_response(user_input)
        print("PyBot:", response)

if __name__ == "__main__":
    chat()




