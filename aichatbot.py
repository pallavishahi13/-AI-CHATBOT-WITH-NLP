import nltk
import numpy as np
import random
import string  # to process standard python strings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample corpus
corpus = """Hello! How can I help you?
I am a chatbot built with Python and NLTK.
You can ask me questions related to programming.
I can talk about Python, Java, or general concepts.
What is Python?
Python is a high-level, interpreted programming language.
Who developed Python?
Guido van Rossum developed Python.
What is Java?
Java is a popular object-oriented programming language.
Thank you.
You're welcome!
Bye
Goodbye! Have a great day!
"""

# Tokenization
sent_tokens = nltk.sent_tokenize(corpus)
word_tokens = nltk.word_tokenize(corpus)

# Preprocessing function
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def Normalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greeting response
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = ["Hi there!", "Hello!", "Hey!", "Hi!", "Nice to meet you!"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Chatbot response function
def response(user_input):
    robo_response = ''
    sent_tokens.append(user_input)
    
    TfidfVec = TfidfVectorizer(tokenizer=Normalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if req_tfidf == 0:
        robo_response = "I'm sorry, I don't understand that."
    else:
        robo_response = sent_tokens[idx]
    
    sent_tokens.pop()
    return robo_response

# Main loop
def chatbot():
    print("Chatbot: Hello! I'm your assistant. Type 'bye' to exit.")
    while True:
        user_input = input("You: ").lower()
        if user_input == 'bye':
            print("Chatbot: Goodbye! Have a nice day.")
            break
        elif greeting(user_input) is not None:
            print("Chatbot:", greeting(user_input))
        else:
            print("Chatbot:", response(user_input))

# Run chatbot
if _name_ == "_main_":
    chatbot()
