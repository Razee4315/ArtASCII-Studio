import os
import pytest
from PIL import Image
import numpy as np
from ascii_converter import ASCIIConverter

def test_ascii_converter_initialization():
    """Test ASCIIConverter initialization with default parameters."""
    test_image_path = 'tests/test_image.png'
    
    # Create a test image if it doesn't exist
    if not os.path.exists(test_image_path):
        test_image = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
        test_image.save(test_image_path)
    
    converter = ASCIIConverter(test_image_path)
    
    assert converter.output_width == 100
    assert converter.density == "medium"
    assert converter.brightness == 1.0
    assert converter.contrast == 1.0
    assert not converter.invert

def test_ascii_conversion():
    """Test basic ASCII conversion functionality."""
    test_image_path = 'tests/test_image.png'
    
    # Create a test image if it doesn't exist
    if not os.path.exists(test_image_path):
        test_image = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
        test_image.save(test_image_path)
    
    converter = ASCIIConverter(test_image_path, output_width=50)
    ascii_art = converter.convert_to_ascii()
    
    assert isinstance(ascii_art, str)
    assert len(ascii_art.split('\n')) > 0

def test_image_transformations():
    """Test various image transformation parameters."""
    test_image_path = 'tests/test_image.png'
    
    # Create a test image if it doesn't exist
    if not os.path.exists(test_image_path):
        test_image = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
        test_image.save(test_image_path)
    
    # Test different parameters
    test_cases = [
        {"brightness": 1.5, "contrast": 1.2, "invert": True},
        {"density": "fine", "detail_preservation": 0.9},
        {"brightness": 0.8, "contrast": 0.7}
    ]
    
    for case in test_cases:
        converter = ASCIIConverter(test_image_path, **case)
        ascii_art = converter.convert_to_ascii()
        assert isinstance(ascii_art, str)
        assert len(ascii_art.split('\n')) > 0
