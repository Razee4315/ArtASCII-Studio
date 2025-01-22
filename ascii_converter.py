from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='ascii_converter.log',
                    filemode='w')

class ASCIIConverter:
    def __init__(self, image_path, output_width=100, density="medium", color=False, 
                 brightness=1.0, contrast=1.0, invert=False, detail_preservation=0.7):
        logging.info(f"Initializing ASCIIConverter with params: "
                     f"image_path={image_path}, output_width={output_width}, "
                     f"density={density}, color={color}, brightness={brightness}, "
                     f"contrast={contrast}, invert={invert}, "
                     f"detail_preservation={detail_preservation}")
        
        self.image_path = image_path
        self.output_width = output_width
        self.density = density
        self.color = color
        self.brightness = brightness
        self.contrast = contrast
        self.invert = invert
        self.detail_preservation = detail_preservation
        self.ascii_chars = self._get_ascii_chars()

    def _get_ascii_chars(self):
        """Return ASCII characters based on density and detail level."""
        detailed_chars = "@%#*+=-:. "
        sparse_chars = "@#%*+=-:. "
        
        if self.density == "fine":
            return detailed_chars
        elif self.density == "coarse":
            return sparse_chars
        else:  # medium
            return "@#%*+=-:. "

    def _resize_image(self, image):
        """Resize the image while maintaining aspect ratio."""
        width, height = image.size
        aspect_ratio = height / width
        new_height = int(self.output_width * aspect_ratio * 0.55)  # Adjust for font aspect ratio
        return image.resize((self.output_width, new_height), Image.LANCZOS)

    def _adjust_image(self, image):
        """Advanced image adjustment with edge preservation."""
        # Apply edge enhancement to preserve details
        edge_enhanced = image.filter(ImageFilter.EDGE_ENHANCE)
        
        # Brightness and contrast adjustment
        enhancer = ImageEnhance.Brightness(edge_enhanced)
        image = enhancer.enhance(self.brightness)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(self.contrast)
        
        # Invert if needed
        if self.invert:
            image = Image.eval(image, lambda x: 255 - x)
        
        return image

    def _advanced_pixel_to_ascii(self, pixel, intensity_map):
        """Convert a pixel to an ASCII character with shape preservation."""
        try:
            r, g, b = pixel[:3]
            
            # Calculate luminance with more nuanced approach
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            
            # Use intensity map for more accurate character selection
            max_chars = len(self.ascii_chars) - 1
            intensity_index = int(luminance * max_chars)
            
            # Incorporate detail preservation
            detail_factor = self.detail_preservation
            if intensity_map is not None and isinstance(intensity_map, np.ndarray):
                # Ensure valid indexing
                intensity_index = min(max(0, intensity_index), intensity_map.shape[0] - 1)
                local_intensity = intensity_map[intensity_index]
                intensity_index = int(intensity_index * (1 - detail_factor) + local_intensity * detail_factor)
            
            # Ensure final index is within bounds
            intensity_index = min(max(0, intensity_index), max_chars)
            
            return self.ascii_chars[intensity_index]
        
        except Exception as e:
            logging.error(f"Error in pixel to ASCII conversion: {e}", exc_info=True)
            # Return a default character if conversion fails
            return self.ascii_chars[len(self.ascii_chars) // 2]

    def _create_intensity_map(self, image):
        """Create an intensity map that preserves local image details."""
        try:
            # Convert image to grayscale
            gray_image = image.convert('L')
            gray_array = np.array(gray_image, dtype=np.float32)
            
            # Apply Gaussian blur to reduce noise
            blurred = gray_image.filter(ImageFilter.GaussianBlur(radius=1))
            blurred_array = np.array(blurred, dtype=np.float32)
            
            # Compute local intensity variations using more efficient method
            height, width = gray_array.shape
            intensity_map = np.zeros_like(gray_array)
            
            # Use sliding window for local intensity calculation
            window_size = 3
            half_window = window_size // 2
            
            for y in range(half_window, height - half_window):
                for x in range(half_window, width - half_window):
                    local_region = blurred_array[
                        y - half_window:y + half_window + 1, 
                        x - half_window:x + half_window + 1
                    ]
                    # Calculate local variation using standard deviation
                    intensity_map[y, x] = np.std(local_region)
            
            # Normalize intensity map
            if intensity_map.max() > intensity_map.min():
                intensity_map = (intensity_map - intensity_map.min()) / (intensity_map.max() - intensity_map.min())
            
            return intensity_map
        
        except Exception as e:
            logging.error(f"Error creating intensity map: {e}", exc_info=True)
            # Return a uniform map if computation fails
            return np.ones_like(np.array(image.convert('L')), dtype=np.float32) * 0.5

    def convert_to_ascii(self):
        """Convert the image to ASCII art with advanced shape preservation."""
        try:
            logging.info(f"Starting image conversion: {self.image_path}")
            
            # Open and prepare the image
            image = Image.open(self.image_path).convert("RGB")
            logging.info(f"Image opened. Original size: {image.size}")
            
            image = self._resize_image(image)
            logging.info(f"Image resized. New size: {image.size}")
            
            image = self._adjust_image(image)
            logging.info("Image adjusted")
            
            # Create intensity map for detail preservation
            intensity_map = self._create_intensity_map(image)
            logging.info(f"Intensity map created. Shape: {intensity_map.shape if intensity_map is not None else 'None'}")
            
            # Convert image to pixel data
            pixels = list(image.getdata())
            logging.info(f"Total pixels: {len(pixels)}")
            
            # Convert pixels to ASCII
            ascii_art = []
            for i in range(image.height):
                row = []
                for j in range(image.width):
                    pixel_index = i * image.width + j
                    pixel = pixels[pixel_index]
                    
                    # Safely get local intensity
                    if intensity_map is not None:
                        local_intensity = intensity_map[min(i, intensity_map.shape[0]-1), 
                                                       min(j, intensity_map.shape[1]-1)]
                    else:
                        local_intensity = None
                    
                    row.append(self._advanced_pixel_to_ascii(pixel, local_intensity))
                ascii_art.append(''.join(row))
            
            logging.info("Image conversion completed successfully")
            return '\n'.join(ascii_art)
        
        except Exception as e:
            logging.error(f"Error converting image: {e}", exc_info=True)
            return f"Error converting image: {e}"
