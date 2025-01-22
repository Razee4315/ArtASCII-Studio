from setuptools import setup, find_packages

setup(
    name="ArtASCII-Studio",
    version="0.1.0",
    author="Saqlain Abbas",
    author_email="your.email@example.com",  # Replace with your email
    description="An advanced image-to-ASCII art conversion tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Razee4315/ArtASCII-Studio",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.7',
        'Pillow>=9.5.0',
        'numpy>=1.24.3'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'artascii-studio=main:main',
        ],
    },
)
