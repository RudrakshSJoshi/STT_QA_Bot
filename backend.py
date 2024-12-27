import os
import io
import wave
import base64
from pydub import AudioSegment
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Import CORS
from faster_whisper import WhisperModel

from Agents.LLM_agent import get_query_response
from Agents.Question_Summarizer import summarize_conversation_to_question
from Agents.RAG_agent import RAG_Agent_Answer
from Agents.WebScrape_agent import WebScrape_Agent_Answer
from Agents.Context_Classifer import classify_context

# Initialize Flask app and Flask-SocketIO
app = Flask(__name__)

# Enable CORS for the entire app to allow requests from localhost:3000
CORS(app, origins=["http://localhost:3000"])  # Allow only the React app

socketio = SocketIO(app)  # Initialize SocketIO with Flask app

# Configure Flask-SocketIO to allow cross-origin requests from 'http://localhost:3000'
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Initialize the Whisper model (can be adjusted)
model = WhisperModel("small", device="cpu", compute_type="float32")

# Function to convert incoming audio to WAV
def convert_audio(input_data):
    try:
        audio = AudioSegment.from_file(io.BytesIO(input_data))
        wav_audio = io.BytesIO()
        audio.export(wav_audio, format="wav")
        wav_audio.seek(0)  # Reset pointer to the beginning of the BytesIO object
        return wav_audio
    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {e}")

# Function to process the audio and return transcription
def transcribe_audio(audio_data):
    # Convert audio to WAV format
    wav_audio = convert_audio(audio_data)
    
    # Save the temporary audio file to disk (for WhisperModel)
    temp_path = "temp_audio.wav"
    with open(temp_path, "wb") as temp_file:
        temp_file.write(wav_audio.read())
    
    # Transcribe the audio
    segments, _ = model.transcribe(temp_path, beam_size=5, best_of=5, language="en")
    transcribed_text = " ".join([segment.text for segment in segments])
    
    # Clean up temporary file
    os.remove(temp_path)
    
    return transcribed_text

# WebSocket event to handle incoming audio
@socketio.on('TranscriptAudio')
def handle_audio(data):
    try:
        print("Received EndPoint Request TranscriptAudio")
        # Decode the base64-encoded audio
        audio_data = base64.b64decode(data['audioData'])
        
        # Transcribe the audio
        transcription = transcribe_audio(audio_data)
        
        # Send back the transcription to the client (no need to include 'person')
        emit('TranscriptResult', {'transcript': transcription})

    except Exception as e:
        print("Error processing audio:", e)
        emit('error', {'message': str(e)})

# WebSocket event for a new connection
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# WebSocket event for disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# REST endpoint to trigger AI logic
@app.route('/AI_Trigger', methods=['POST'])
def ai_trigger():
    conversation = request.json.get('conversation')
    print('Received conversation:', conversation)
    print('\n\n')

    summarised_question = summarize_conversation_to_question(conversation)
    print("Summarised Question:", summarised_question)
    print('\n\n')

    implemented_context = ''
    context_classification = classify_context(summarised_question)
    if '1' in context_classification:
        implemented_context = 'Personal Query Detected, Implementing RAG Agent'
        print("Personal Query Detected, Implementing RAG Agent")
        response = RAG_Agent_Answer(summarised_question)
    elif '2' in context_classification:
        implemented_context = 'WebScraping Query Detected, Implementing WebScrape Agent'
        print("WebScraping Query Detected, Implementing WebScrape Agent")
        response = WebScrape_Agent_Answer(summarised_question)
    else:
        implemented_context = 'General Query Detected, Implementing LLM Agent'
        print("General Query Detected, Implementing LLM Agent")
        response = get_query_response(summarised_question)
        print("Response:", response)
    return jsonify({"query": summarised_question, "context": implemented_context, "response": response})

# Starting the Flask server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
