import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def classify_context(question):
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
    prompt = f"""Your aim is to classify the question into one of the 3 categories:
1. Personal Question
2. Web Scraping Question
3. LLM Answerable question

You should always think from the perspective of the person answering the question.
Any question asking to introduce oneself should be a personal question, and not related to LLM, as you should be in the feet of the person answering the question.
If the question asks about questions specific to a person and his/her work related stuff, you should classify it as a personal question by responding with '1'.
Personal questions include explaining work experience, education, skills, past jobs, teamwork, etc.
If the question asks something where internet is required to know the answer, you should classify it as a web scraping question by responding with '2'.
Web scraping questions include questions about companies, products, services, stock prices, current affairs, etc.
If the question can be answered by an LLM such as yours, then you classify it as an LLM answerable question by responding with '3'.
LLM answerable questions include questions about general knowledge, health, history, anything where your knwoledge base can answer, etc.

NOTE: It is important that your response is only a single digit 1, 2 or 3.
Question: {question}"""

    # Create the message payload
    messages = [{"role": "user", "content": prompt}]

    # Fetch the response
    response = google_model.invoke(messages)
    return response.content.strip()