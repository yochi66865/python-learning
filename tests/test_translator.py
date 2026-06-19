import json
from src.translator import EnglishToHebrewTranslator
from pathlib import Path


def test_translate_file(tmp_path):
    translator = EnglishToHebrewTranslator.__new__(
        EnglishToHebrewTranslator
    )

    # 🔥 MOCK ONLY THE CORE LOGIC
    translator.translate_text = lambda text: {
        "Hello": "שלום",
        "World": "עולם"
    }[text]

    segments_file = tmp_path / "segments.json"
    output_file = tmp_path / "translated.json"

    segments = [
        {
            "start": 0,
            "end": 1,
            "text": "Hello"
        },
        {
            "start": 1,
            "end": 2,
            "text": "World"
        }
    ]

    with open(segments_file, "w", encoding="utf-8") as file:
        json.dump(segments, file, ensure_ascii=False)

    output_path = translator.translate_or_load(
        segments_path=str(segments_file),
        output_path=str(output_file)
    )

    output_file = Path(output_path)
    assert output_file.exists()

    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]["he"] == "שלום"
    assert data[1]["he"] == "עולם"