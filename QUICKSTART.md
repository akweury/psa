# Quick Start Guide

This guide will help you get started with PSA video processor quickly.

## Quick Setup (5 minutes)

### Option 1: Docker (Recommended for Servers)

1. **Clone and configure**:
   ```bash
   git clone https://github.com/akweury/psa.git
   cd psa
   cp .env.example .env
   ```

2. **Edit `.env` to point to your video folder**:
   ```bash
   # Edit this line to your actual video path
   VIDEO_PATH=/path/to/your/videos
   ```

3. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

   The application will:
   - Process all videos in your specified folder
   - Generate logic rules in `./data/output/`
   - Create logs in `./data/output/psa.log`

### Option 2: Local Python (Recommended for Development)

1. **Clone and setup**:
   ```bash
   git clone https://github.com/akweury/psa.git
   cd psa
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure**:
   ```bash
   cp config/config.example.yaml config/config.yaml
   ```
   
   Edit `config/config.yaml` and set your video path:
   ```yaml
   video:
     input_path: "/path/to/your/videos"
   ```

3. **Run**:
   ```bash
   python src/main.py
   ```

## What Happens Next?

The application will:

1. **Scan** your video folder for supported formats (mp4, avi, mov, mkv)
2. **Process** each video frame by frame
3. **Extract** logic rules based on the AI model
4. **Save** results in the output directory

## Output Files

After processing, you'll find:

```
data/output/
├── psa.log                    # Processing logs
├── video1_rules.json          # Logic rules for video1
├── video2_rules.json          # Logic rules for video2
└── ...
```

## Example Output

```json
{
  "video": "example.mp4",
  "total_rules": 5,
  "generated_at": "2024-10-22T13:30:00",
  "rules": [
    {
      "rule_id": "rule_0001",
      "rule_type": "brightness",
      "description": "Dark frame detected at frame 100",
      "confidence": 0.95,
      "frame_number": 100,
      "timestamp": 3.33
    }
  ]
}
```

## Customizing the AI Model

The default implementation includes a simple brightness detector as an example. To use your own AI model:

1. Open `src/main.py`
2. Find the `process_frame()` function
3. Replace the example code with your AI model inference:

```python
def process_frame(frame_number, frame, rules_manager, video_metadata):
    # Your AI model here
    predictions = your_model.predict(frame)
    
    # Create rules based on predictions
    for prediction in predictions:
        rules_manager.create_rule(
            rule_type=prediction.type,
            description=prediction.description,
            confidence=prediction.confidence,
            frame_number=frame_number,
            metadata=prediction.data
        )
```

## Configuration Tips

### Processing Every 10th Frame (Faster)
```yaml
processing:
  frame_skip: 10  # Process every 10th frame
```

### Limit Frames for Testing
```yaml
processing:
  max_frames: 100  # Only process first 100 frames
```

### Save Extracted Frames
```yaml
output:
  save_frames: true
  frames_path: "./data/output/frames"
```

### Change Output Format
```yaml
output:
  rules_format: "yaml"  # or "json" or "txt"
```

## Troubleshooting

### "Video path does not exist"
- Check that the path in your config is correct
- Ensure the path is accessible from inside the container (for Docker)

### "No video files found"
- Verify your video files have supported extensions (.mp4, .avi, .mov, .mkv)
- Check file permissions

### Docker volume issues
- Ensure the VIDEO_PATH in .env is an absolute path
- On Windows, use forward slashes: `C:/Users/Videos`

## Next Steps

1. Review the full [README.md](README.md) for detailed documentation
2. Customize the AI model in `src/main.py`
3. Adjust configuration in `config/config.yaml`
4. Add your own logic rule types and processing logic

## Support

For issues or questions, please open an issue on GitHub.
