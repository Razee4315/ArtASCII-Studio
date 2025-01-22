import argparse
from ascii_converter import ASCIIConverter

def main():
    parser = argparse.ArgumentParser(description="Convert images to ASCII art.")
    parser.add_argument("image_path", help="Path to the input image")
    parser.add_argument("--output", "-o", help="Output file path (default: print to console)")
    parser.add_argument("--width", "-w", type=int, default=100, help="Output width (default: 100)")
    parser.add_argument("--density", "-d", choices=["fine", "medium", "coarse"], default="medium", help="Density of ASCII art")
    args = parser.parse_args()

    converter = ASCIIConverter(args.image_path, output_width=args.width, density=args.density)
    ascii_art = converter.convert_to_ascii()

    if args.output:
        with open(args.output, "w") as file:
            file.write(ascii_art)
    else:
        print(ascii_art)

if __name__ == "__main__":
    main()
