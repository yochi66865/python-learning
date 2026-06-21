import json
from pathlib import Path

from src.hebrew_tts import HebrewTtsService


async def fake_generate(
    text,
    output_file
):
    output_file.write_text("dummy")


def test_generate_from_file(tmp_path):
    service = HebrewTtsService()

    service.generate_audio = fake_generate

    translated_file = tmp_path / "test_translated.json"

    json.dump(
        [
            {
                "start": 0,
                "end": 1,
                "en": "Hello",
                "he": "שלום"
            },
            {
                "start": 1,
                "end": 2,
                "en": "World",
                "he": "עולם"
            }
        ],
        open(
            translated_file,
            "w",
            encoding="utf-8"
        ),
        ensure_ascii=False
    )

    import asyncio

    files = asyncio.run(
        service.generate_from_file(
            translated_file,
            tmp_path / "tts"
        )
    )

    print(f"Generated files: {files}")

    assert len(files) == 2
    assert files[0].exists()
    assert files[1].exists()