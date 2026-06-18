import logging
from moviepy import VideoFileClip
import whisper
from pathlib import Path


# -----------------------------
# Logging setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class VideoToTextPipeline:
    def __init__(self, model_size="base"):
        logger.info(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)

    # -----------------------------
    def load_video(self, video_path: str):
        logger.info(f"Loading video: {video_path}")
        return VideoFileClip(video_path)

    # -----------------------------
    def extract_audio(self, video_path: str, audio_output_path: str):
        logger.info("Extracting audio from video...")

        video = self.load_video(video_path)
        audio = video.audio

        Path(audio_output_path).parent.mkdir(parents=True, exist_ok=True)

        audio.write_audiofile(audio_output_path)

        logger.info(f"Audio saved to: {audio_output_path}")
        return audio_output_path

    # -----------------------------
    def transcribe_audio(self, audio_path: str):
        logger.info(f"Transcribing audio: {audio_path}")

        result = self.model.transcribe(audio_path, language="en")
        logger.info("Transcription completed")
        return result["text"]

    # -----------------------------
    def save_text(self, text: str, output_path: str):
        logger.info(f"Saving transcription to: {output_path}")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        logger.info("Text file saved successfully")

    # -----------------------------
    def process_video_to_text(self, video_path: str, target_folder: str):
        logger.info("Starting full pipeline...")

        target = Path(target_folder)

        audio_path = target / "extracted_audio.mp3"
        text_path = target / "transcription.txt"

        if audio_path.exists():
            logger.info(f"Audio already exists: {audio_path}. Skipping extraction.")
        else:
            self.extract_audio(video_path, str(audio_path))
        
        if text_path.exists():
            logger.info(f"Transcription already exists: {text_path}. Skipping transcription.")
        else:
            text = self.transcribe_audio(str(audio_path))
            self.save_text(text, str(text_path))

        logger.info("Pipeline completed successfully")

        return str(text_path)