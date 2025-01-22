import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QSlider, QFileDialog, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget,
    QComboBox, QLineEdit, QCheckBox, QMessageBox, QDialog, QVBoxLayout, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from ascii_converter import ASCIIConverter
from PIL import Image, ImageFilter, ImageOps

class ImageTransformDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Image Transformations")
        self.setGeometry(200, 200, 300, 200)
        
        layout = QVBoxLayout()
        
        # Filter group
        filter_group = QButtonGroup(self)
        self.blur_radio = QRadioButton("Blur")
        self.sharpen_radio = QRadioButton("Sharpen")
        self.edge_enhance_radio = QRadioButton("Edge Enhance")
        self.contour_radio = QRadioButton("Contour")
        
        filter_group.addButton(self.blur_radio)
        filter_group.addButton(self.sharpen_radio)
        filter_group.addButton(self.edge_enhance_radio)
        filter_group.addButton(self.contour_radio)
        
        layout.addWidget(self.blur_radio)
        layout.addWidget(self.sharpen_radio)
        layout.addWidget(self.edge_enhance_radio)
        layout.addWidget(self.contour_radio)
        
        # Apply button
        apply_btn = QPushButton("Apply Transformation")
        apply_btn.clicked.connect(self.accept)
        layout.addWidget(apply_btn)
        
        self.setLayout(layout)
        
    def get_selected_filter(self):
        if self.blur_radio.isChecked():
            return ImageFilter.BLUR
        elif self.sharpen_radio.isChecked():
            return ImageFilter.SHARPEN
        elif self.edge_enhance_radio.isChecked():
            return ImageFilter.EDGE_ENHANCE
        elif self.contour_radio.isChecked():
            return ImageFilter.CONTOUR
        return None

class ArtASCIIStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_image_path = None
        self.current_image = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ArtASCII Studio")
        self.setGeometry(100, 100, 1000, 800)

        # Load retro font
        QFontDatabase.addApplicationFont("assets/retro_font.ttf")
        self.retro_font = QFont("Retro Gaming", 10)

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Image display
        self.image_label = QLabel("Drag and drop an image here", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed #ccc; padding: 20px;")
        self.image_label.setAcceptDrops(True)
        self.image_label.dragEnterEvent = self.drag_enter_event
        self.image_label.dropEvent = self.drop_event
        layout.addWidget(self.image_label)

        # ASCII art display
        self.ascii_display = QTextEdit(self)
        self.ascii_display.setFont(self.retro_font)
        self.ascii_display.setReadOnly(True)
        layout.addWidget(self.ascii_display)

        # Controls
        controls_layout = QHBoxLayout()

        # Density slider
        self.density_slider = QSlider(Qt.Horizontal)
        self.density_slider.setMinimum(1)
        self.density_slider.setMaximum(3)
        self.density_slider.setValue(2)
        self.density_slider.setTickInterval(1)
        self.density_slider.setTickPosition(QSlider.TicksBelow)
        controls_layout.addWidget(QLabel("Density:"))
        controls_layout.addWidget(self.density_slider)

        # Brightness slider
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(200)
        self.brightness_slider.setValue(100)
        controls_layout.addWidget(QLabel("Brightness:"))
        controls_layout.addWidget(self.brightness_slider)

        # Contrast slider
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(200)
        self.contrast_slider.setValue(100)
        controls_layout.addWidget(QLabel("Contrast:"))
        controls_layout.addWidget(self.contrast_slider)

        # Invert checkbox
        self.invert_checkbox = QCheckBox("Invert Colors", self)
        controls_layout.addWidget(self.invert_checkbox)

        # Theme selector
        self.theme_selector = QComboBox(self)
        self.theme_selector.addItems(["Green-on-Black", "Amber-on-Black", "White-on-Black"])
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        controls_layout.addWidget(self.theme_selector)

        # Export buttons
        self.export_txt_btn = QPushButton("Export as TXT", self)
        self.export_txt_btn.clicked.connect(self.export_txt)
        controls_layout.addWidget(self.export_txt_btn)

        self.export_img_btn = QPushButton("Export as Image", self)
        self.export_img_btn.clicked.connect(self.export_image)
        controls_layout.addWidget(self.export_img_btn)

        self.copy_btn = QPushButton("Copy to Clipboard", self)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        controls_layout.addWidget(self.copy_btn)

        # Add Update Image and Transform Image buttons to controls layout
        self.update_image_btn = QPushButton("Update Image", self)
        self.update_image_btn.clicked.connect(self.update_image)
        controls_layout.addWidget(self.update_image_btn)
        
        self.transform_image_btn = QPushButton("Transform Image", self)
        self.transform_image_btn.clicked.connect(self.transform_image)
        controls_layout.addWidget(self.transform_image_btn)

        # Detail preservation slider
        self.detail_slider = QSlider(Qt.Horizontal)
        self.detail_slider.setMinimum(0)
        self.detail_slider.setMaximum(100)
        self.detail_slider.setValue(70)  # Default 70% detail preservation
        self.detail_slider.setTickInterval(10)
        self.detail_slider.setTickPosition(QSlider.TicksBelow)
        controls_layout.addWidget(QLabel("Detail Preservation:"))
        controls_layout.addWidget(self.detail_slider)

        layout.addLayout(controls_layout)
        main_widget.setLayout(layout)

        # Connect sliders to live preview
        self.density_slider.valueChanged.connect(self.update_ascii_art)
        self.brightness_slider.valueChanged.connect(self.update_ascii_art)
        self.contrast_slider.valueChanged.connect(self.update_ascii_art)
        self.invert_checkbox.stateChanged.connect(self.update_ascii_art)
        self.detail_slider.valueChanged.connect(self.update_ascii_art)

    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        image_path = event.mimeData().urls()[0].toLocalFile()
        self.process_image(image_path)

    def process_image(self, image_path):
        """Convert the image to ASCII and display it."""
        self.current_image_path = image_path
        pixmap = QPixmap(image_path).scaled(400, 400, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.update_ascii_art()

    def update_ascii_art(self):
        """Update the ASCII art based on current settings."""
        if not self.current_image_path:
            return
        
        density = ["coarse", "medium", "fine"][self.density_slider.value() - 1]
        brightness = self.brightness_slider.value() / 100
        contrast = self.contrast_slider.value() / 100
        invert = self.invert_checkbox.isChecked()
        detail_preservation = self.detail_slider.value() / 100  # New detail preservation parameter
        
        converter = ASCIIConverter(
            self.current_image_path,
            density=density,
            brightness=brightness,
            contrast=contrast,
            invert=invert,
            detail_preservation=detail_preservation  # Pass detail preservation
        )
        ascii_art = converter.convert_to_ascii()
        self.ascii_display.setPlainText(ascii_art)

    def change_theme(self, theme):
        """Change the UI theme."""
        theme_mapping = {
            "Green-on-Black": "green_theme.css",
            "Amber-on-Black": "amber_theme.css", 
            "White-on-Black": "white_theme.css"
        }
        theme_file = os.path.join("assets", theme_mapping.get(theme, "green_theme.css"))
        try:
            with open(theme_file, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Theme file not found: {theme_file}")

    def export_txt(self):
        """Export ASCII art as a .txt file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save ASCII Art", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.ascii_display.toPlainText())

    def export_image(self):
        """Export ASCII art as an image."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save ASCII Art", "", "PNG Files (*.png);;JPG Files (*.jpg)")
        if file_path:
            from PIL import Image, ImageDraw, ImageFont
            ascii_text = self.ascii_display.toPlainText()
            font = ImageFont.load_default()
            image = Image.new("RGB", (800, 600), "white")
            draw = ImageDraw.Draw(image)
            draw.text((10, 10), ascii_text, font=font, fill="black")
            image.save(file_path)

    def copy_to_clipboard(self):
        """Copy ASCII art to clipboard."""
        QApplication.clipboard().setText(self.ascii_display.toPlainText())
        QMessageBox.information(self, "Copied", "ASCII art copied to clipboard!")

    def update_image(self):
        """Open a file dialog to select and update the image."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            self.process_image(file_path)

    def transform_image(self):
        """Open transformation dialog and apply selected filter."""
        if not self.current_image_path:
            QMessageBox.warning(self, "No Image", "Please load an image first.")
            return
        
        dialog = ImageTransformDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_filter = dialog.get_selected_filter()
            if selected_filter:
                try:
                    # Open the original image
                    image = Image.open(self.current_image_path)
                    
                    # Apply the selected filter
                    transformed_image = image.filter(selected_filter)
                    
                    # Save the transformed image
                    temp_path = os.path.join(os.path.dirname(self.current_image_path), 
                                             f"transformed_{os.path.basename(self.current_image_path)}")
                    transformed_image.save(temp_path)
                    
                    # Process the transformed image
                    self.process_image(temp_path)
                    
                except Exception as e:
                    QMessageBox.critical(self, "Transformation Error", str(e))

def main():
    app = QApplication(sys.argv)
    window = ArtASCIIStudio()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
