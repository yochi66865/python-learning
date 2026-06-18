import os
from unittest.mock import MagicMock
from src.audio_extractor import VideoToTextPipeline


def test_save_text(tmp_path):
    pipeline = VideoToTextPipeline.__new__(VideoToTextPipeline)

    text = "hello world"
    output_file = tmp_path / "output.txt"

    pipeline.save_text(text, str(output_file))

    assert os.path.exists(output_file)

    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == text


def test_transcribe_audio_mock():
    pipeline = VideoToTextPipeline.__new__(VideoToTextPipeline)

    # mock whisper model
    pipeline.model = MagicMock()
    pipeline.model.transcribe.return_value = {"text": "mock transcript"}

    result = pipeline.transcribe_audio("fake.mp3")

    assert result == "mock transcript"