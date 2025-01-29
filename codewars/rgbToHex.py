#!/usr/bin/env python3

def rgbToHex(r, g, b):
    """Converts RGB values to a hex color string."""
    hexString = f"#{r:02x}{g:02x}{b:02x}"
    return hexString.lower()


def main():
    hex_color = rgbToHex(255, 255, 255)
    print(hex_color)  # Prints: #ffffff


if __name__ == '__main__':
    main()
