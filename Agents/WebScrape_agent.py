import json
import os
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def search_internet(query):
    """Search the internet about a given topic and return relevant results."""
    top_result_to_return = 10
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)

    # Check if there is an 'organic' key in the response
    if 'organic' not in response.json():
        return "Sorry, I couldn't find anything about that. There could be an error with your SerpApi key."

    results = response.json()['organic']
    result_string = []
    for result in results[:top_result_to_return]:
        try:
            result_string.append('\n'.join([
                f"Title: {result['title']}",
                f"Link: {result['link']}",
                f"Snippet: {result['snippet']}",
                "\n-----------------"
            ]))
        except KeyError:
            continue  # Skip results that don't have the expected keys

    return '\n'.join(result_string)

def WebScrape_Agent_Answer(question):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Initialize the Google Generative AI model
    google_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )

    context = search_internet(question)

    # Define the prompt for summarizing to a question
    prompt = prompt = f"""Given a question and the context,
you are supposed to answer the question as if you are providing the answer based on your own understanding.
Do not explicitly refer to the context as if it's external.
Treat the context as if it is part of your own knowledge,
and respond as though you are personally answering the question,
without referencing the fact that you're drawing from the context.
Your answer should be in the first person.

Question:
{question}

Context:
{context}"""

    # Create the message payload
    # print(prompt)
    messages = [{"role": "user", "content": prompt}]

    # Fetch the summarized question
    response = google_model.invoke(messages)
    return response.content.strip()