# ImageCraft

Gut Bug is a Python-based application designed for advanced image manipulation tasks. The program offers features such as background removal, background replacement, and image segmentation, all through a user-friendly console interface.

## Features

1. **Remove Background**  
   Effortlessly remove the background from an image and save the result as a transparent PNG file.

2. **Change Background**  
   Replace the background of an image with a custom image.

3. **Image Segmentation**  
   Use instance segmentation to identify and manipulate specific objects or segments within an image.  
   - Remove specific objects (segments).  
   - Extract or retain specific objects.

## Prerequisites

- **Python 3.7 or higher**
- Required Python libraries:
  - `rembg`
  - `Pillow`
  - `easygui`
  - `pixellib`
  - `opencv-python`
  - `numpy`

You can install the required libraries using the following command:
```bash
pip install rembg pillow easygui pixellib opencv-python numpy
