"""Tests for configuration loader."""

import os
import pytest
import tempfile
import yaml
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config_loader import ConfigLoader


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        'video': {
            'input_path': '/test/videos',
            'formats': ['.mp4', '.avi']
        },
        'processing': {
            'frame_skip': 2,
            'max_frames': 100
        },
        'output': {
            'output_path': '/test/output'
        }
    }


@pytest.fixture
def config_file(sample_config):
    """Create a temporary config file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(sample_config, f)
        config_path = f.name
    
    yield config_path
    
    # Cleanup
    os.unlink(config_path)


def test_config_loader_initialization(config_file):
    """Test ConfigLoader initialization."""
    loader = ConfigLoader(config_file)
    assert loader.config_path == config_file
    assert loader.config is not None


def test_config_loader_get_value(config_file):
    """Test getting configuration values."""
    loader = ConfigLoader(config_file)
    
    assert loader.get('video.input_path') == '/test/videos'
    assert loader.get('processing.frame_skip') == 2
    assert loader.get('nonexistent.key', 'default') == 'default'


def test_config_loader_sections(config_file):
    """Test getting configuration sections."""
    loader = ConfigLoader(config_file)
    
    video_config = loader.get_video_config()
    assert video_config['input_path'] == '/test/videos'
    assert video_config['formats'] == ['.mp4', '.avi']
    
    processing_config = loader.get_processing_config()
    assert processing_config['frame_skip'] == 2
    assert processing_config['max_frames'] == 100


def test_config_loader_file_not_found():
    """Test error handling for missing config file."""
    with pytest.raises(FileNotFoundError):
        ConfigLoader('/nonexistent/config.yaml')


def test_config_loader_invalid_yaml():
    """Test error handling for invalid YAML."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("invalid: yaml: content: {")
        config_path = f.name
    
    try:
        with pytest.raises(ValueError):
            ConfigLoader(config_path)
    finally:
        os.unlink(config_path)
