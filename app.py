from services.video_processor import VideoProcessor


def main():

    processor = VideoProcessor()

    processor.process_video(
        "data/videos/input.mp4",
        "data/output/output.mp4"
    )


if __name__ == "__main__":
    main()