"""Video processor for extracting and processing frames."""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional, Generator
import logging


class VideoProcessor:
    """Process videos frame by frame for analysis."""

    def __init__(self, config: dict):
        """
        Initialize video processor.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

    def get_video_files(self, video_path: str) -> List[Path]:
        """
        Get all video files from the specified path.

        Args:
            video_path: Path to video directory

        Returns:
            List of video file paths
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            self.logger.error(f"Video path does not exist: {video_path}")
            return []

        formats = self.config.get('formats', ['.mp4', '.avi', '.mov', '.mkv'])
        video_files = []

        if video_path.is_file():
            if video_path.suffix.lower() in formats:
                video_files.append(video_path)
        else:
            for format_ext in formats:
                video_files.extend(video_path.glob(f"*{format_ext}"))
                video_files.extend(video_path.glob(f"*{format_ext.upper()}"))

        self.logger.info(f"Found {len(video_files)} video files")
        return sorted(video_files)

    def extract_frames(
        self, 
        video_path: str,
        frame_skip: int = 1,
        max_frames: int = 0,
        resize: Optional[Tuple[int, int]] = None
    ) -> Generator[Tuple[int, np.ndarray], None, None]:
        """
        Extract frames from video.

        Args:
            video_path: Path to video file
            frame_skip: Process every Nth frame
            max_frames: Maximum number of frames to process (0 = all)
            resize: Tuple of (width, height) to resize frames

        Yields:
            Tuple of (frame_number, frame_image)
        """
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            self.logger.error(f"Failed to open video: {video_path}")
            return

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        self.logger.info(
            f"Processing video: {Path(video_path).name} "
            f"({total_frames} frames, {fps:.2f} FPS)"
        )

        frame_count = 0
        processed_count = 0

        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break

                # Skip frames according to frame_skip parameter
                if frame_count % frame_skip != 0:
                    frame_count += 1
                    continue

                # Resize if specified
                if resize is not None:
                    frame = cv2.resize(frame, resize)

                yield frame_count, frame
                
                processed_count += 1
                frame_count += 1

                # Stop if max_frames reached
                if max_frames > 0 and processed_count >= max_frames:
                    break

        finally:
            cap.release()
            self.logger.info(f"Processed {processed_count} frames from video")

    def save_frame(self, frame: np.ndarray, output_path: str) -> bool:
        """
        Save a single frame to disk.

        Args:
            frame: Frame image as numpy array
            output_path: Path to save the frame

        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, frame)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save frame: {e}")
            return False

    def get_video_metadata(self, video_path: str) -> dict:
        """
        Extract metadata from video file.

        Args:
            video_path: Path to video file

        Returns:
            Dictionary containing video metadata
        """
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            return {}

        metadata = {
            'filename': Path(video_path).name,
            'path': str(video_path),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'duration_seconds': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
        }

        cap.release()
        return metadata
