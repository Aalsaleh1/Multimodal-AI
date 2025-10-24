import os
from openai import OpenAI
import google.generativeai

# Use environment variables or securely load API keys from config files
open_api_key = os.getenv('OPENAI_API_KEY')  # Set your OpenAI key in the environment
google_api_key = os.getenv('GOOGLE_API_KEY')  # Set your Google Gemini key in the environment

if open_api_key:
    print("OpenAI key exists and begins with", open_api_key[:5])
else:
    print("OpenAI key does not exist")

if google_api_key:
    print("Google Gemini key exists and begins with", google_api_key[:5])
else:
    print("Google Gemini key does not exist")

# Initialize OpenAI client
openai = OpenAI(api_key=open_api_key)

# Define system and user prompts
system_message = "You are an assistant that is great at genAI"
user_prompt = "What are multimodal AIs?"

prompts = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_prompt}
]

# Example using OpenAI API (gpt-4o-mini)
completion = openai.chat.completions.create(model='gpt-4o-mini', messages=prompts)
print("OpenAI response:", completion.choices[0].message.content)

# Example with temperature adjustment
completion = openai.chat.completions.create(
    model='gpt-4o-mini',
    messages=prompts,
    temperature=0.4
)
print("OpenAI response with temperature adjustment:", completion.choices[0].message.content)

# Initialize Gemini client (Google's generative AI model)
gemini_via_openai_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = gemini_via_openai_client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=prompts
)
print("Google Gemini response:", response.choices[0].message.content)

# Streaming OpenAI responses (display in Markdown format)
stream = openai.chat.completions.create(
    model='gpt-4.1-mini',
    messages=prompts,
    temperature=0.7,
    stream=True
)

reply = ""
for chunk in stream:
    reply += chunk.choices[0].delta.content or ''
    reply = reply.replace("```", "")  # Clean any code block formatting
    print(reply)  # Print the response

# Let's make a conversation between GPT-4.1-mini and Gemini
# Using cheaper models to minimize costs

gpt_model = "gpt-4.1-mini"
gemini_model = "gemini-2.5-flash"

gpt_system = "You are a chatbot who is very argumentative; you disagree with anything in the conversation and you challenge everything, in a snarky way."
gemini_system = "You are a very polite, courteous chatbot. You try to agree with everything the other person says, or find common ground. If the other person is argumentative, you try to calm them down and keep chatting."

gpt_messages = ["hi"]
gemini_messages = ["كيف الجو اليوم"]

def call_gpt():
    messages = [{"role": "system", "content": gpt_system}]
    for gpt, gemini in zip(gpt_messages, gemini_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": gemini})

    completion = openai.chat.completions.create(
        model=gpt_model,
        messages=messages
    )
    print("GPT-4.1-mini response:", completion.choices[0].message.content)

call_gpt()
