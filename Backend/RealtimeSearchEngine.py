from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values, load_dotenv
import os

# Loading environment variables
env_vars = dotenv_values(".env")
# load_dotenv()  # If using .env for environment variables
Username = env_vars.get("Username", "")
Assistantname = env_vars.get("Assistantname", "")
Agentsex = env_vars.get("Agentsex", "")
GroqAPIKey = env_vars.get("GroqAPIKey", "") # Ensure you have this key properly

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate, fast, and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional way, human-like, naturally-sounding, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***
*** Give short and concise answer until asked to explain or to tell anything in detail. ***"""

# Initialize chat log
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
    messages = []

def GoogleSearch(query):
    results = list(search(query, num_results=5))  # Searching the query and limiting to 5 results
    Answer = f"The search results for '{query}' are:\n[start]\n"
    
    for i in results:
        Answer += f"URL: {i}\n"  # The result is a URL string; you can add more details if needed
    
    Answer += "[end]"
    # print(Answer)
    return Answer
    
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)
    
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    return data

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    messages.append({"role": "user", "content": f"{prompt}"})

    # Append the Google search result
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Create a completion request with the information
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()  # Clean up SystemChatBot
    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))