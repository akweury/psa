"""Main entry point for PSA video processor."""

import os
import sys
import logging
from pathlib import Path

from config_loader import ConfigLoader
from video_processor import VideoProcessor
from logic_rules import LogicRulesManager


def setup_logging(config: dict):
    """
    Setup logging configuration.

    Args:
        config: Logging configuration dictionary
    """
    log_level = getattr(logging, config.get('level', 'INFO'))
    log_format = config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = config.get('file')

    # Create output directory for log file
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
    else:
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[logging.StreamHandler(sys.stdout)]
        )


def process_frame(frame_number: int, frame, rules_manager: LogicRulesManager, video_metadata: dict):
    """
    Process a single frame and extract logic rules.
    
    This is a placeholder function that should be customized based on your AI model.

    Args:
        frame_number: Current frame number
        frame: Frame image as numpy array
        rules_manager: LogicRulesManager instance
        video_metadata: Video metadata dictionary
    """
    # TODO: Implement your AI model logic here
    # This is an example of how to create rules
    
    # Example: Detect if frame is dark or bright
    import numpy as np
    mean_brightness = np.mean(frame)
    
    if mean_brightness < 50:
        rules_manager.create_rule(
            rule_type="brightness",
            description=f"Dark frame detected at frame {frame_number}",
            confidence=0.95,
            frame_number=frame_number,
            timestamp=frame_number / video_metadata.get('fps', 30),
            metadata={'mean_brightness': float(mean_brightness)}
        )
    elif mean_brightness > 200:
        rules_manager.create_rule(
            rule_type="brightness",
            description=f"Bright frame detected at frame {frame_number}",
            confidence=0.95,
            frame_number=frame_number,
            timestamp=frame_number / video_metadata.get('fps', 30),
            metadata={'mean_brightness': float(mean_brightness)}
        )


def process_video(video_path: Path, config_loader: ConfigLoader, logger: logging.Logger):
    """
    Process a single video file.

    Args:
        video_path: Path to video file
        config_loader: ConfigLoader instance
        logger: Logger instance
    """
    logger.info(f"Processing video: {video_path.name}")

    # Get configuration
    video_config = config_loader.get_video_config()
    processing_config = config_loader.get_processing_config()
    output_config = config_loader.get_output_config()

    # Initialize components
    video_processor = VideoProcessor(video_config)
    rules_manager = LogicRulesManager(output_config)

    # Get video metadata
    metadata = video_processor.get_video_metadata(str(video_path))
    logger.info(f"Video metadata: {metadata}")

    # Process frames
    frame_skip = processing_config.get('frame_skip', 1)
    max_frames = processing_config.get('max_frames', 0)
    resize = processing_config.get('resize')
    save_frames = output_config.get('save_frames', False)
    frames_path = output_config.get('frames_path', './data/output/frames')

    frame_count = 0
    for frame_number, frame in video_processor.extract_frames(
        video_path=str(video_path),
        frame_skip=frame_skip,
        max_frames=max_frames,
        resize=resize
    ):
        # Process frame with AI model
        process_frame(frame_number, frame, rules_manager, metadata)

        # Optionally save frame
        if save_frames:
            frame_output_path = Path(frames_path) / video_path.stem / f"frame_{frame_number:06d}.jpg"
            video_processor.save_frame(frame, str(frame_output_path))

        frame_count += 1

    logger.info(f"Processed {frame_count} frames")

    # Save logic rules
    rules_manager.save_rules(video_path.name)
    logger.info(f"Extracted {len(rules_manager.rules)} logic rules")


def main():
    """Main function."""
    # Load configuration
    try:
        config_loader = ConfigLoader()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please create a configuration file at config/config.yaml")
        sys.exit(1)

    # Setup logging
    logging_config = config_loader.get_logging_config()
    setup_logging(logging_config)
    logger = logging.getLogger(__name__)

    logger.info("Starting PSA Video Processor")

    # Get video configuration
    video_config = config_loader.get_video_config()
    video_input_path = video_config.get('input_path')

    if not video_input_path:
        logger.error("Video input path not configured")
        sys.exit(1)

    # Initialize video processor to get video files
    video_processor = VideoProcessor(video_config)
    video_files = video_processor.get_video_files(video_input_path)

    if not video_files:
        logger.warning("No video files found to process")
        sys.exit(0)

    # Process each video
    for video_path in video_files:
        try:
            process_video(video_path, config_loader, logger)
        except Exception as e:
            logger.error(f"Error processing video {video_path.name}: {e}", exc_info=True)

    logger.info("PSA Video Processor completed")


if __name__ == "__main__":
    main()
