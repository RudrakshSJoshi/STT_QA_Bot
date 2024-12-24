from audio_transcription import process_audio_conversation
from Agents.LLM_agent import get_query_response
from Agents.Question_Summarizer import summarize_conversation_to_question
from Agents.RAG_agent import RAG_Agent_Answer
from Agents.WebScrape_agent import WebScrape_Agent_Answer
from Agents.Context_Classifer import classify_context

# Audio Transcription IMPLEMENTED SUCCESSFULLY
# process_audio_conversation(0, "SampleSound.wav")  # For interviewer
# process_audio_conversation(1, "SampleSound2.mp3")  # For interviewee

# LLM_agent IMPLEMENTED SUCCESSFULLY
# query = "What is the largest planet in our solar system?"
# response = get_query_response(query)
# print("Response:", response)

# Question_Summarizer IMPLEMENTED SUCCESSFULLY
# response = summarize_conversation_to_question()
# print(response)

# RAG_agent IMPLEMENTED SUCCESSFULLY
# response = RAG_Agent_Answer("What is your current education status?")
# print(response)

# WebScrape_agent IMPLEMENTED SUCCESSFULLY
# response = WebScrape_Agent_Answer("What is the current stock value of Tesla and Apple?")
# print(response)

# # Context_Classifer IMPLEMENTED SUCCESSFULLY
# response = classify_context("Explain what all previous internships you have done?")
# print(response)
