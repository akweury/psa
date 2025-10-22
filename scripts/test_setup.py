#!/usr/bin/env python3
"""
Test setup script to verify PSA installation and configuration.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import cv2
        import numpy
        import yaml
        from config_loader import ConfigLoader
        from video_processor import VideoProcessor
        from logic_rules import LogicRulesManager
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        from config_loader import ConfigLoader
        config = ConfigLoader('config/config.yaml')
        video_path = config.get('video.input_path')
        print(f"✓ Configuration loaded successfully")
        print(f"  Video path: {video_path}")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_output_directory():
    """Test that output directory can be created."""
    print("\nTesting output directory...")
    try:
        output_dir = Path('data/output')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Test write permission
        test_file = output_dir / '.test'
        test_file.write_text('test')
        test_file.unlink()
        
        print(f"✓ Output directory accessible: {output_dir.absolute()}")
        return True
    except Exception as e:
        print(f"✗ Output directory test failed: {e}")
        return False


def test_video_path():
    """Test video input path accessibility."""
    print("\nTesting video path...")
    try:
        from config_loader import ConfigLoader
        config = ConfigLoader('config/config.yaml')
        video_path = Path(config.get('video.input_path'))
        
        if video_path.exists():
            print(f"✓ Video path exists: {video_path}")
            
            # Try to list files
            try:
                files = list(video_path.glob('*'))
                print(f"  Found {len(files)} items in directory")
            except PermissionError:
                print("  ⚠ Permission denied to list directory contents")
        else:
            print(f"⚠ Video path does not exist: {video_path}")
            print("  This is expected if you haven't configured it yet")
        
        return True
    except Exception as e:
        print(f"✗ Video path test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("PSA Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_configuration,
        test_output_directory,
        test_video_path
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("\n✓ All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Configure your video path in config/config.yaml")
        print("2. Run: python src/main.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that config/config.yaml exists")
        print("3. Verify file permissions")
        return 1


if __name__ == "__main__":
    sys.exit(main())
