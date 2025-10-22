"""Configuration loader for PSA video processor."""

import os
import yaml
from typing import Dict, Any


class ConfigLoader:
    """Load and manage configuration from YAML file."""

    def __init__(self, config_path: str = None):
        """
        Initialize configuration loader.

        Args:
            config_path: Path to configuration YAML file
        """
        if config_path is None:
            config_path = os.environ.get('CONFIG_PATH', 'config/config.yaml')
        
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Returns:
            Dictionary containing configuration
        """
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing configuration file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key (supports dot notation).

        Args:
            key: Configuration key (e.g., 'video.input_path')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value

    def get_video_config(self) -> Dict[str, Any]:
        """Get video configuration section."""
        return self.config.get('video', {})

    def get_processing_config(self) -> Dict[str, Any]:
        """Get processing configuration section."""
        return self.config.get('processing', {})

    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration section."""
        return self.config.get('output', {})

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration section."""
        return self.config.get('logging', {})

    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration section."""
        return self.config.get('model', {})
