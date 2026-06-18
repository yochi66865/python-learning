from audio_extractor import VideoToTextPipeline


if __name__ == "__main__":
    pipeline = VideoToTextPipeline(model_size="base")

    video_path = "assets/Throat_Exercises_for_Snoring.mp4"
    target_folder = "output"

    output_file = pipeline.process_video_to_text(video_path, target_folder)

    print("Saved transcription at:", output_file)