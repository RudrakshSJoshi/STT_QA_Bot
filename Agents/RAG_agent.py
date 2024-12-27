import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def RAG_Agent_Answer(question, user_path="user_data.txt"):
    # Load environment variables
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Initialize the Google Generative AI model
    google_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )

    # Read the user data from the file
    with open(user_path, 'r') as file:
        user_info = file.read().strip()
    
    # print(user_info)

    # Define the prompt for summarizing to a question
    prompt = f"""Given a question and the person's data, you are supposed to answer the question based on the person's data,
and in first person, as if you yourself are the person answering the question.
The question and user data are strictly monitored, so hallucination will negatively impact your score, only answer what is present in the data.
User Data:
{user_info}
Question:
{question}"""

    # Create the message payload
    # print(prompt)
    messages = [{"role": "user", "content": prompt}]

    # Fetch the summarized question
    response = google_model.invoke(messages)
    return response.content.strip()