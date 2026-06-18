import json
from unittest.mock import MagicMock
from src.audio_extractor import VideoToTextPipeline

def test_transcribe_audio_returns_segments():
    pipeline = VideoToTextPipeline.__new__(VideoToTextPipeline)

    pipeline.model = MagicMock()
    pipeline.model.transcribe.return_value = {
        "segments": [
            {"start": 0.0, "end": 1.5, "text": " Hello "},
            {"start": 1.5, "end": 3.0, "text": " world "}
        ]
    }

    result = pipeline.transcribe_audio("fake.mp3")

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0]["text"] == "Hello"
    assert result[0]["start"] == 0.0


def test_save_segments(tmp_path):
    pipeline = VideoToTextPipeline.__new__(VideoToTextPipeline)

    segments = [
        {"start": 0, "end": 1, "text": "hello"}
    ]

    output_file = tmp_path / "segments.json"

    pipeline.save_segments(segments, str(output_file))

    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data[0]["text"] == "hello"