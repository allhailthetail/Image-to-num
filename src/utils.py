# Imports:
import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter # used by preprocess_image()

def preprocess_image(input_path, output_path=None, crop_tuple=None):
    '''
    Description:
    Function processes the image before it's sent to Tesseract for text extraction.

    1. Image is resized so fewer pixels need to be analyzed (efficiency bump)
    2. Crop to relevant area
    3. Convert from color to B/W
    4. Invert colors (Black text on White bg is optimal)
    5. Gaussian blur decreases number of artifacts/dust
    6. Contrast is increased to further darken the text

    Parameters:
    input_path (str): File being processed
    output_path=None (str): Output can be changed if desired...
    crop_tuple=None  (tup: Int): Cropping coordinates

    Output:
    processed (PIL.Image.Image): Enhanced/adjusted image object
    '''

    # First open the image
    img = Image.open(input_path).convert("RGB")

    # Scale the image down to fewer pixels for processing efficiency:
    BASE_WIDTH = 800 # (const) Target width (default recommended: 800px)
    orig_width, orig_height = img.size

    # Maintain aspect ratio by scaling proportionately
    scale_ratio = BASE_WIDTH / float(orig_width)
    new_height = int(orig_height * scale_ratio)

    # Finally, resize the image with pillow:
    img = img.resize((BASE_WIDTH, new_height), Image.Resampling.LANCZOS)

    # Crop it
    # NOTE: (From the Pillow docs)
    #   The Python Imaging Library uses a Cartesian pixel coordinate system, with (0,0) in the upper left corner.
    #   Note that the coordinates refer to the implied pixel corners; the centre of a pixel addressed as (0, 0)
    #   actually lies at (0.5, 0.5).
    #   Coordinates are usually passed to the library as 2-tuples (x, y). Rectangles are represented as 4-tuples,
    #   (x1, y1, x2, y2), with the upper left corner given first.
    #   A good reference: (80, 240, 640, 450) at time of development...

    # Only crop if cropping coordinates are provided
    if crop_tuple:
        # Crops to the tuple provided to the function
        img = img.crop(crop_tuple)

    # Convert to gray scale
    img = img.convert("L")

    # Invert the colors
    img = ImageOps.invert(img)

    # apply Gaussian blur
    img = img.filter(ImageFilter.GaussianBlur(1.5)) # 3.5 optimal, 1.5 seems to work fine

    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(15) # 10 optimal

    if output_path:
        img.save(output_path)

    return img


if __name__ == "__main__":
    '''
    Main Program:

    input [stdin]:
    arg1: input image location (.jpeg)
    arg2: processed image location (.jpeg)
    '''

    if len(sys.argv) < 2:
        print("Not enough arguments")
        sys.exit(1)

    input_img = sys.argv[1]
    output_img = None
    if len(sys.argv) > 2:
        output_img = sys.argv[2]

    processed_img = preprocess_image(input_img, output_path=output_img)
    print("Processing Complete.")
