import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def summarize_conversation_to_question(file_path = "conversation.txt"):
    # Load environment variables
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Initialize the Google Generative AI model
    google_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )

    # Read the conversation from the file
    with open(file_path, 'r') as file:
        conversation = file.read().strip()

    # Define the prompt for summarizing to a question
    prompt = f"""Given the following conversation flow between an interviewer and an interviewee, 
rephrase the entire dialog into a single question based on the last dialog segment. 
Ensure that the rephrased question contains no discrepancies and is clear and precise. 
Conversation:
{conversation}"""

    # Create the message payload
    # print(prompt)
    messages = [{"role": "user", "content": prompt}]

    # Fetch the summarized question
    response = google_model.invoke(messages)
    return response.content.strip()