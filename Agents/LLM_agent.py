import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def get_query_response(question):
    # Load environment variables
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Initialize the Google Generative AI model
    google_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )

    # Define the prompt
    prompt = f"""Answer the Query in about 50-60 words. The query is -> {question}"""

    # Create the message payload
    messages = [{"role": "user", "content": prompt}]

    # Fetch the response
    response = google_model.invoke(messages)
    return response.content.strip()