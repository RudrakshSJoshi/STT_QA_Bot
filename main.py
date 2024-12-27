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
# response = summarize_conversation_to_question("Hello Rudraksh, so what is your current education status?")
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

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for the entire app to allow requests from localhost:3000
CORS(app, origins=["http://localhost:3000"])  # Allow only the React app

socketio = SocketIO(app)  # Initialize SocketIO with Flask app

# Configure Flask-SocketIO to allow cross-origin requests from 'http://localhost:3000'
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

@app.route('/AI_Trigger', methods=['POST'])
def ai_trigger():
    conversation = request.json.get('conversation')
    print('Received conversation:', conversation)
    
    # Process the conversation, possibly send it to an AI model
    ai_response = "This is the AI's response based on the conversation."
    
    return jsonify({"response": ai_response})

# WebSocket event for receiving audio and returning transcript
@socketio.on('TranscriptAudio')
def handle_audio(data):
    # Process the audio data and generate a transcript
    print(f"Received audio data: {data}")
    
    # Example: send a dummy transcript back
    transcript = "This is the transcribed text."
    emit('TranscriptResult', {'transcript': transcript})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)  # Use `socketio.run()` instead of `app.run()`