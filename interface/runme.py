import openai
import os

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize the chat context
context = ""

# Loop for multiple requests
while True:
    # Get user input
    user_input = input("Ask your question (or 'quit'): ")

    if (user_input == "quit"): break

    print("The current context is: ", context)
    print("The user_input is: ", user_input)
    
    # Send request to ChatGPT API with the current context
    response = openai.Completion.create(
        engine="davinci",
        prompt=context + user_input,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Get the generated response from ChatGPT
    message = response.choices[0].text.strip()

    # Print the response 
    print("ChatGPT:", message)

    # Update the context to continue conversation
    context += user_input + message
