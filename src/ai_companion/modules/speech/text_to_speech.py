import io
import os
from typing import Optional

from ai_companion.core.exceptions import TextToSpeechError
from ai_companion.settings import settings
from elevenlabs import ElevenLabs


class TextToSpeech:
    """A class to handle text-to-speech conversion using ElevenLabs."""

    REQUIRED_ENV_VARS = ["ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID"]

    def __init__(self):
        self._validate_env_vars()
        self._client: Optional[ElevenLabs] = None

    def _validate_env_vars(self) -> None:
        missing_vars = [var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @property
    def client(self) -> ElevenLabs:
        if self._client is None:
            self._client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        return self._client

    async def synthesize(self, text: str) -> bytes:
        """Convert text to speech using the ElevenLabs SDK."""
        if not text.strip():
            raise ValueError("Input text cannot be empty")
        if len(text) > 5000:
            raise ValueError("Input text exceeds maximum length of 5000 characters")
        try:
            # SDK v1+: text_to_speech is a client object, call .convert() on it
            audio_generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=settings.ELEVENLABS_VOICE_ID,
                model_id=settings.TTS_MODEL_NAME,
                output_format="mp3_44100_128",
            )

            # convert() returns a generator of bytes chunks — collect them
            buffer = io.BytesIO()
            for chunk in audio_generator:
                if chunk:
                    buffer.write(chunk)

            audio_bytes = buffer.getvalue()
            if not audio_bytes:
                raise TextToSpeechError("Generated audio is empty")
            return audio_bytes

        except TextToSpeechError:
            raise
        except Exception as e:
            raise TextToSpeechError(f"Text-to-speech conversion failed: {str(e)}") from e