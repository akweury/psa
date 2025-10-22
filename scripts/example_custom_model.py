#!/usr/bin/env python3
"""
Example: How to customize the AI model for video processing.

This example demonstrates how to integrate your own AI model
into the PSA video processing pipeline.
"""

import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config_loader import ConfigLoader
from video_processor import VideoProcessor
from logic_rules import LogicRulesManager


class CustomAIModel:
    """
    Example custom AI model class.
    Replace this with your actual AI model.
    """
    
    def __init__(self):
        """Initialize your model here."""
        print("Initializing custom AI model...")
        # Load your trained model
        # self.model = load_model('path/to/model.pth')
        
    def predict(self, frame):
        """
        Run inference on a single frame.
        
        Args:
            frame: numpy array of shape (H, W, 3)
            
        Returns:
            List of predictions with type, description, confidence
        """
        # Example: Simple color detection
        predictions = []
        
        # Calculate average color
        avg_color = np.mean(frame, axis=(0, 1))
        r, g, b = avg_color
        
        # Detect dominant color
        if r > g and r > b and r > 150:
            predictions.append({
                'type': 'color_detection',
                'description': 'Red dominant color detected',
                'confidence': 0.9,
                'data': {'rgb': [int(r), int(g), int(b)]}
            })
        elif g > r and g > b and g > 150:
            predictions.append({
                'type': 'color_detection',
                'description': 'Green dominant color detected',
                'confidence': 0.9,
                'data': {'rgb': [int(r), int(g), int(b)]}
            })
        elif b > r and b > g and b > 150:
            predictions.append({
                'type': 'color_detection',
                'description': 'Blue dominant color detected',
                'confidence': 0.9,
                'data': {'rgb': [int(r), int(g), int(b)]}
            })
        
        # Example: Motion detection (simplified)
        if hasattr(self, 'previous_frame') and self.previous_frame is not None:
            diff = np.mean(np.abs(frame.astype(float) - self.previous_frame.astype(float)))
            if diff > 30:
                predictions.append({
                    'type': 'motion',
                    'description': f'Significant motion detected (diff: {diff:.2f})',
                    'confidence': min(diff / 100, 1.0),
                    'data': {'frame_difference': float(diff)}
                })
        
        self.previous_frame = frame.copy()
        
        return predictions


def process_frame_custom(frame_number, frame, rules_manager, video_metadata, model):
    """
    Custom frame processing function using your AI model.
    
    Args:
        frame_number: Current frame number
        frame: Frame image as numpy array
        rules_manager: LogicRulesManager instance
        video_metadata: Video metadata dictionary
        model: Your custom AI model instance
    """
    # Run your model inference
    predictions = model.predict(frame)
    
    # Create logic rules from predictions
    for pred in predictions:
        rules_manager.create_rule(
            rule_type=pred['type'],
            description=pred['description'],
            confidence=pred['confidence'],
            frame_number=frame_number,
            timestamp=frame_number / video_metadata.get('fps', 30),
            metadata=pred.get('data', {})
        )


def main():
    """Main function demonstrating custom model integration."""
    print("PSA Custom Model Example")
    print("=" * 50)
    
    # Load configuration
    config_loader = ConfigLoader('config/config.yaml')
    
    # Initialize your custom model
    custom_model = CustomAIModel()
    
    # Get video configuration
    video_config = config_loader.get_video_config()
    processing_config = config_loader.get_processing_config()
    output_config = config_loader.get_output_config()
    
    # Initialize components
    video_processor = VideoProcessor(video_config)
    rules_manager = LogicRulesManager(output_config)
    
    # For this example, let's create a simple test video path
    # In practice, you would get this from your video files
    video_input_path = video_config.get('input_path')
    video_files = video_processor.get_video_files(video_input_path)
    
    if not video_files:
        print("No video files found. Please configure your video path.")
        print("For testing, you can use any sample video file.")
        return
    
    # Process first video as example
    video_path = video_files[0]
    print(f"\nProcessing: {video_path.name}")
    
    # Get video metadata
    metadata = video_processor.get_video_metadata(str(video_path))
    print(f"Video info: {metadata['frame_count']} frames, {metadata['fps']:.2f} FPS")
    
    # Process frames
    frame_skip = processing_config.get('frame_skip', 1)
    max_frames = processing_config.get('max_frames', 100)  # Limit for example
    
    print(f"\nProcessing frames (skip={frame_skip}, max={max_frames})...")
    
    for frame_number, frame in video_processor.extract_frames(
        video_path=str(video_path),
        frame_skip=frame_skip,
        max_frames=max_frames
    ):
        # Process with your custom model
        process_frame_custom(frame_number, frame, rules_manager, metadata, custom_model)
        
        if frame_number % 10 == 0:
            print(f"  Processed frame {frame_number}...")
    
    print(f"\nExtracted {len(rules_manager.rules)} logic rules")
    
    # Save results
    rules_manager.save_rules(video_path.name)
    print(f"Results saved to: {output_config['output_path']}")
    
    # Display some example rules
    print("\nExample rules:")
    for rule in rules_manager.rules[:5]:
        print(f"  - [{rule.rule_type}] {rule.description} (confidence: {rule.confidence:.2f})")


if __name__ == "__main__":
    main()
