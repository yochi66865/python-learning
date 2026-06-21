import json
from pathlib import Path
import edge_tts
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

class HebrewTtsService:

    VOICE = "he-IL-AvriNeural"

    async def generate_audio(
        self,
        text: str,
        output_file: Path
    ):
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.VOICE
        )

        await communicate.save(str(output_file))

    async def generate_from_file(
        self,
        translated_file_path: str,
        output_dir_path: str
    ):
        output_dir = Path(output_dir_path)
        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        translated_file = Path(translated_file_path)

        with open(
            translated_file,
            encoding="utf-8"
        ) as file:
            segments = json.load(file)

        generated_files = []

        for index, segment in enumerate(segments):

            audio_file = (
                output_dir /
                f"segment_{index:04}.mp3"
            )

            if audio_file.exists():
                logger.info(
                    f"Skipping {audio_file}"
                )

                generated_files.append(
                    audio_file
                )

                continue

            logger.info(
                f"Generating audio "
                f"{index + 1}/{len(segments)}"
            )

            await self.generate_audio(
                segment["he"],
                audio_file
            )

            generated_files.append(
                audio_file
            )

        return generated_files