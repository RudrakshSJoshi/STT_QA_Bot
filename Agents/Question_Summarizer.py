import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def summarize_conversation_to_question(conversation: str):
    """
    Given a conversation as a string, summarize it into a single question based on the last dialog segment.

    Args:
    - conversation (str): The entire conversation between the interviewer and the interviewee.

    Returns:
    - str: A summarized question based on the last dialog segment.
    """
    # Load environment variables
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Initialize the Google Generative AI model
    google_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )

    # Define the prompt for summarizing the conversation into a question
    prompt = f"""
You are stateless AI model which will not use previous input or previous generated outputs for answering the next queries.    
Given the following conversation flow between an interviewer and an interviewee, 
rephrase the entire dialog into a single question based on the last dialog segments. 
You should depend mostly on the last segments of the conversation, because that part constructs the summarised question.
Ensure that the rephrased question contains no discrepancies and is clear and precise. 
Always focus on the last segment of the conversation as it holds the maximum information regarding the summarised question.
Conversation:
{conversation}"""

    # Create the message payload
    messages = [{"role": "user", "content": prompt}]

    # Fetch the summarized question
    response = google_model.invoke(messages)
    return response.content.strip()
