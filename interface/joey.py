#!/usr/bin/env python3

import openai
import os
import re
import requests
from bs4 import BeautifulSoup

# Check that the API key was provided
if "OPENAI_API_KEY" not in os.environ:
    print("Error: Please set the OPENAI_API_KEY environment variable.")
    exit(1)

# Set up OpenAI API client
openai.api_key = os.environ["OPENAI_API_KEY"]

def find_url(input_str):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    url = re.findall(url_pattern, input_str)
    return url[0] if url else None

def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([p.get_text() for p in paragraphs])
    return content

def send_query(input, context):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            { "role": "system", "content": context },
            { "role": "user", "content": input }
        ],
        temperature=0.7,
    )

    response_text = response['choices'][0]['message']['content'].strip()
    return response_text

# Set up conversation context
context = "Please make your responses very conversational and polite"
while True:
    print("\nWhat's on your mind? (Type 'exit' to quit)")
    input_str = input(">>> ")

    if input_str == "exit":
        print("Goodbye!")
        exit(0)
    elif input_str == "clear":
        os.system('clear')
        continue

    url = find_url(input_str)
    if url:
        try:
            article_content = fetch_article_content(url)
            input_str = f"{input_str} {article_content}"
        except Exception as e:
            print(f"Error fetching the article: {e}")
            continue

    response = send_query(input_str, context)

    print("\n", response)

    context = f"{context}\nUser: {input_str}\nAI: {response}"
    context = context.replace("\n", "")

