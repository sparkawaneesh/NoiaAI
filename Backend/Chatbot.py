from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
Agentsex = env_vars.get("Agentsex")
GroqAPIKey = env_vars.get("GroqAPIKey", "")

if not GroqAPIKey:
    raise ValueError("GroqAPIKey not found in .env file")

client = Groq(api_key=GroqAPIKey)

# Ensure the Data directory exists
os.makedirs("Data", exist_ok=True)
CHAT_LOG_FILE = "Data/ChatLog.json"

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet. You are a {Agentsex} Agent.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [{"role": "system", "content": System}]

def realtime_information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use the realtime information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n "
    return data

def answer_modifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def chatbot(query):
    messages = []  

    try:
        try:
            with open(CHAT_LOG_FILE, "r") as f:
                messages = load(f)
        except FileNotFoundError:
            with open(CHAT_LOG_FILE, "w") as f:
                dump([], f, indent=4)

        messages.append({"role": "user", "content": query})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": realtime_information()}] + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": answer})

        with open(CHAT_LOG_FILE, "w") as f:
            dump(messages, f, indent=4)

        return answer_modifier(answer)

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred. Please try again later."

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        response = chatbot(user_input)
        print(response)
        print("-" * 50) 