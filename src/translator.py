import json
import logging
from transformers import MarianMTModel, MarianTokenizer
from pathlib import Path

logger = logging.getLogger(__name__)

class EnglishToHebrewTranslator:
    MODEL_NAME = "Helsinki-NLP/opus-mt-en-he"

    def __init__(self):
        logger.info("Loading translation model...")

        self.tokenizer = MarianTokenizer.from_pretrained(
            self.MODEL_NAME
        )

        self.model = MarianMTModel.from_pretrained(
            self.MODEL_NAME
        )

        logger.info("Translation model loaded")

    def translate_or_load(
        self,
        segments_path: str,
        output_path: str
    ) -> str:

        translation_file = Path(output_path)

        if translation_file.exists():
            logger.info(
                f"Translations already exist: "
                f"{translation_file}. "
                f"Skipping translation."
            )

            return output_path

        return self.translate( segments_path, output_path )

    
    def translate(
        self,
        segments_path: str,
        output_path: str
    ) -> str:

        logger.info("loading segments for translation")
        segments = self.load_json(segments_path)
        
        logger.info("Starting translation")
        translations = self.translate_segments(
            segments
        )
        
        self.save_translations(
            translations,
            output_path
        )

        return output_path
    
    def load_json(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def translate_text(self, text: str) -> str:
        logger.debug(f"Translating text: {text}")

        tokens = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        translated = self.model.generate(**tokens)

        result = self.tokenizer.decode(
            translated[0],
            skip_special_tokens=True
        )

        logger.debug(f"Translation result: {result}")

        return result

    def translate_segments(self, segments: list[dict]) -> list[dict]:
        logger.info(
            f"Translating {len(segments)} segments"
        )

        translated_segments = []

        for segment in segments:
            translated_text = self.translate_text(
                segment["text"]
            )

            translated_segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "en": segment["text"],
                "he": translated_text
            })

        logger.info("Segment translation completed")

        return translated_segments
    
    def save_translations(
        self,
        translations: list,
        output_path: str
    ):
        logger.info(
            f"Saving translations to {output_path}"
        )

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                translations,
                file,
                ensure_ascii=False,
                indent=2
            )

        logger.info("Translations saved")