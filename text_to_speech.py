"""
Convert text to British-accented speech using Google Cloud TTS
"""
import logging
import os
from google.cloud import texttospeech
from config import (
    TTS_LANGUAGE_CODE, TTS_VOICE_NAME, TTS_SPEECH_RATE, 
    TTS_PITCH, TEMP_DIR
)

logger = logging.getLogger(__name__)


class TextToSpeech:
    """Convert text to speech with British accent"""
    
    def __init__(self):
        """Initialize Google Cloud TTS client"""
        try:
            self.client = texttospeech.TextToSpeechClient()
            self.language_code = TTS_LANGUAGE_CODE
            self.voice_name = TTS_VOICE_NAME
        except Exception as e:
            logger.error(f"Failed to initialize TTS client: {e}")
            raise
    
    def synthesize_speech(self, text: str, output_path: str) -> bool:
        """
        Convert text to speech and save as MP3
        
        Args:
            text: text to convert to speech
            output_path: path to save MP3 file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate input
            if not text or not text.strip():
                logger.error("Empty text provided for TTS")
                return False
            
            # Truncate very long text (Google Cloud has limits)
            if len(text) > 5000:
                text = text[:5000] + "..."
                logger.warning("Text truncated to 5000 characters")
            
            # Create synthesis request
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Configure voice
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.language_code,
                name=self.voice_name,
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            
            # Configure audio codec
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=TTS_SPEECH_RATE,
                pitch=TTS_PITCH,
                sample_rate_hertz=48000,
            )
            
            # Perform TTS
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Write audio to file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "wb") as out:
                out.write(response.audio_content)
            
            logger.info(f"Generated speech: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            return False
    
    def get_audio_duration(self, mp3_path: str) -> float:
        """
        Get duration of MP3 file in seconds
        
        Args:
            mp3_path: path to MP3 file
            
        Returns:
            Duration in seconds, or 0 if failed
        """
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_mp3(mp3_path)
            return len(audio) / 1000.0  # Convert ms to seconds
        except Exception as e:
            logger.error(f"Failed to get audio duration: {e}")
            return 0.0
    
    def truncate_text_to_duration(self, text: str, max_duration: int = 30) -> str:
        """
        Estimate and truncate text to fit within max duration
        
        Args:
            text: input text
            max_duration: maximum duration in seconds
            
        Returns:
            Truncated text
        """
        # Rough estimate: ~150 words per minute, ~1 word per 0.4 seconds
        words_per_second = 150 / 60
        max_words = int(max_duration * words_per_second)
        
        words = text.split()
        
        if len(words) > max_words:
            truncated = " ".join(words[:max_words]) + "..."
            logger.info(f"Text truncated from {len(words)} to {max_words} words")
            return truncated
        
        return text


if __name__ == "__main__":
    # Test TTS
    logging.basicConfig(level=logging.INFO)
    
    tts = TextToSpeech()
    
    test_text = "Breaking news from around the world. Technology company announces major breakthrough in artificial intelligence."
    output_file = f"{TEMP_DIR}/test_audio.mp3"
    
    if tts.synthesize_speech(test_text, output_file):
        print(f"✓ Audio generated: {output_file}")
        duration = tts.get_audio_duration(output_file)
        print(f"✓ Duration: {duration:.1f} seconds")
    else:
        print("✗ Failed to generate audio")
