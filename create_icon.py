#!/usr/bin/env python3
"""
Create a simple PNG icon for Break Assistant
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple PNG icon."""
    
    # Create a 256x256 image with green background
    img = Image.new('RGB', (256, 256), color='#4CAF50')
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fallback to default if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 72)
        except:
            font = ImageFont.load_default()
    
    # Draw "BA" text in white
    text = "BA"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (256 - text_width) // 2
    y = (256 - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    # Save the icon
    img.save("break-assistant.png")
    print("Icon created: break-assistant.png")

if __name__ == "__main__":
    create_icon() 