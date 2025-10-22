# PSA - Perceptual-Semantic-Action Loop

A video processing AI model for temporal data reasoning. PSA processes videos frame-by-frame to extract logic rules and patterns from visual data.

## Overview

PSA is designed to:
- Process video files frame by frame
- Apply AI/ML models to extract semantic information
- Generate logic rules based on video content
- Store videos externally (not in git repository)
- Run efficiently on servers using Docker

## Features

- **Frame-by-Frame Processing**: Efficiently extract and process video frames
- **Configurable Video Input**: Specify external video folder paths via configuration
- **Logic Rules Extraction**: Generate structured logic rules from video analysis
- **Multiple Output Formats**: Support for JSON, YAML, and text output
- **Docker Support**: Easy deployment on servers with Docker and docker-compose
- **Flexible Configuration**: YAML-based configuration for all parameters

## Project Structure

```
psa/
├── src/                    # Source code
│   ├── main.py            # Main entry point
│   ├── config_loader.py   # Configuration management
│   ├── video_processor.py # Video processing logic
│   └── logic_rules.py     # Logic rules extraction
├── config/                 # Configuration files
│   ├── config.yaml        # Main configuration
│   └── config.example.yaml # Example configuration
├── tests/                  # Test files
├── data/                   # Data directory (excluded from git)
│   └── output/            # Output directory for results
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker compose configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akweury/psa.git
   cd psa
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   ```bash
   cp config/config.example.yaml config/config.yaml
   # Edit config/config.yaml to set your video path and preferences
   ```

5. **Run the application**:
   ```bash
   python src/main.py
   ```

### Docker Deployment

1. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env to set VIDEO_PATH to your external video folder
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

   Or manually with Docker:
   ```bash
   docker build -t psa-video-processor .
   docker run -v /path/to/videos:/app/videos -v ./data/output:/app/data/output psa-video-processor
   ```

## Configuration

The main configuration file is `config/config.yaml`. Key configuration options:

### Video Input
```yaml
video:
  input_path: "/path/to/videos"  # Path to external video folder
  formats: [".mp4", ".avi", ".mov", ".mkv"]  # Supported formats
```

### Processing Options
```yaml
processing:
  frame_skip: 1        # Process every Nth frame
  max_frames: 0        # Max frames to process (0 = all)
  resize: null         # Resize frames [width, height] or null
```

### Output Configuration
```yaml
output:
  output_path: "./data/output"     # Output directory
  save_frames: false                # Save extracted frames
  rules_format: "json"              # Format: json, yaml, or txt
  include_metadata: true            # Include video metadata
```

### Logging
```yaml
logging:
  level: "INFO"                     # Log level
  file: "./data/output/psa.log"    # Log file path
```

## Usage

### Processing Videos

The application will automatically process all video files in the configured input directory:

```bash
python src/main.py
```

### Customizing the AI Model

The frame processing logic is in `src/main.py` in the `process_frame()` function. Replace this with your AI model:

```python
def process_frame(frame_number, frame, rules_manager, video_metadata):
    # Your AI model inference here
    # Example:
    # predictions = your_model.predict(frame)
    
    # Create rules based on predictions
    rules_manager.create_rule(
        rule_type="detection",
        description="Object detected",
        confidence=0.95,
        frame_number=frame_number,
        metadata={'object_type': 'person'}
    )
```

## Output

The application generates logic rules files in the specified format:

### JSON Output Example
```json
{
  "video": "example.mp4",
  "total_rules": 10,
  "generated_at": "2024-10-22T13:30:00",
  "rules": [
    {
      "rule_id": "rule_0001",
      "rule_type": "detection",
      "description": "Object detected at frame 150",
      "confidence": 0.95,
      "frame_number": 150,
      "timestamp": 5.0,
      "metadata": {}
    }
  ]
}
```

## Testing

Run tests with pytest:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=src tests/
```

## Development

### Adding New Features

1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Submit pull request

### Code Style

Follow PEP 8 guidelines for Python code.

## Docker Notes

- Videos should be mounted from external storage using Docker volumes
- The container runs as a service and processes videos automatically
- Logs and output are stored in mounted volumes for persistence
- Configuration can be updated without rebuilding the image

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or issues, please open an issue on GitHub.
