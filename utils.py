import os

def validate_image_path(image_path):
    """Check if the image path is valid."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    if not image_path.lower().endswith((".png", ".jpg", ".jpeg")):
        raise ValueError("Unsupported image format. Use PNG or JPG.")
