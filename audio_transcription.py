import os
from pydub import AudioSegment
from faster_whisper import WhisperModel


def process_audio_conversation(speaker_type, audio_path, conversation_file="conversation.txt", model_path="small"):
    """
    Transcribe audio and append it to a conversation text file in the format:
    Interviewer: <text>
    Interviewee: <text>

    Args:
        speaker_type (int): 0 for Interviewer, 1 for Interviewee.
        audio_path (str): Path to the audio file.
        conversation_file (str): Path to the conversation text file.
        model_path (str): Path to the Whisper model (default is 'small').
    """

    def convert_audio(input_file, output_file):
        """Convert audio to WAV format with compatible parameters."""
        try:
            audio = AudioSegment.from_file(input_file)
            audio.export(output_file, format="wav")
            return output_file
        except Exception as e:
            raise RuntimeError(f"Audio conversion failed: {e}")

    try:
        # Check if the audio file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"The file '{audio_path}' does not exist.")

        # Ensure file is in WAV format
        file_extension = os.path.splitext(audio_path)[1].lower()
        if file_extension != ".wav":
            wav_file = audio_path.rsplit('.', 1)[0] + ".wav"
            audio_path = convert_audio(audio_path, wav_file)

        # Load the Faster Whisper model
        model = WhisperModel(model_path, device="cpu", compute_type="float32")

        # Transcribe audio
        segments, _ = model.transcribe(audio_path, beam_size=5, best_of=5)
        transcribed_text = " ".join([segment.text for segment in segments])

        # Determine speaker
        speaker = "Interviewer" if speaker_type == 0 else "Interviewee"

        # Append to the conversation file
        with open(conversation_file, "a") as file:
            file.write(f"{speaker}: {transcribed_text}\n")

        print(f"Transcription appended to '{conversation_file}':\n{speaker}: {transcribed_text}")

    except Exception as e:
        print(f"Error: {e}")
