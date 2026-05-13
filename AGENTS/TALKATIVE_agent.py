from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from groq import Groq
import os  
from dotenv import load_dotenv
from pathlib import Path
from logger import get_logger

logger = get_logger(__name__)

class Talkie:
    def __init__(self, audio_file_path=None):
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            logger.critical("Missing API Key")
            raise ValueError("Missing API Key")
        
        self.audio_file_path = audio_file_path
        self.client = Groq(api_key=GROQ_API_KEY)

    def friend(self):
        """Transcribe audio file using Whisper model.
        and genereate audio output
        
        Args:
            audio_file: audio file
        
        Returns:
            Transcribed text from audio and then text to audio
        """
        
        with open(self.audio_file_path, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                file=(self.audio_file_path, file.read()),
                model="whisper-large-v3-turbo",
                temperature=0,
                response_format="verbose_json",
            )
            
            # Save transcription to file
            query_file_path = os.path.dirname(__file__) + "/User_Query.txt"
            with open(query_file_path, "w") as f:
                f.write(transcription.text)
            
            logger.info("Transcription generated successfully")
            voice_input=  transcription.text
            
            llm = self.client.chat.completions
            
            PROMPT = f'''
            You are a helpful bestfriend of me since childhood
            QUERY-
            {voice_input}
            give the answer in less than 50 words 
            '''
            
            response = llm.create(
                model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": PROMPT}
        ]
    )
            final_response = response.choices[0].message.content
            
            speech_file_path = Path(__file__).parent / "speech.wav"
            
            tts_response = self.client.audio.speech.create(
            model="canopylabs/orpheus-v1-english",
            voice="autumn",
            response_format="wav",
            input= final_response,
            )
            logger.info("tts_response generated successfully")

            if hasattr(tts_response, "stream_to_file"):
                tts_response.stream_to_file(speech_file_path)
            elif hasattr(tts_response, "read"):
                speech_file_path.write_bytes(tts_response.read())
            elif isinstance(tts_response, bytes):
                speech_file_path.write_bytes(tts_response)
            else:
                speech_file_path.write_bytes(tts_response.content)

            return {
                "transcription": voice_input,
                "response": final_response,
                "audio_path": str(speech_file_path)
            }
