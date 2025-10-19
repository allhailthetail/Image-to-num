# Imports:
import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter # used by preprocess_image()

def preprocess_image(input_path, output_path=None):
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

    Output:
    processed (PIL.Image.Image): Enhanced/adjusted image object
    '''

    # First open the image
    img = Image.open(input_path).convert("RGB")

    # Smaller resolution (This is to run it on my CPU faster, but on a GPU this part of the code
    # could be removed and the application should work better with a better image resolution)
    base_width = 800 # 800 optimal
    w_percent = (base_width / float(img.size[0]))
    h_size = int((float(img.size[1])* float(w_percent)))
    img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)

    # Crop it
    width, height = img.size
    left = int(0.1 * width) #0.033 For testing images, 0.05 Broken ones,0.1 Latest
    top = int(0.4 * height)
    right = int(0.80 * width) # 0.75 Before # 0.80 optimal
    bottom = int(0.75 * height) # Just height before
    cropped = img.crop((left, top, right, bottom))

    # Convert grayscale
    gray = cropped.convert("L")
    #gray = img.convert("L")

    # Invert the colors
    inverted = ImageOps.invert(gray)

    # apply Gaussian blur
    blurred = inverted.filter(ImageFilter.GaussianBlur(1.5)) # 3.5 optimal, 1.5 seems to work fine

    # Increase contrast
    enhancer = ImageEnhance.Contrast(blurred)
    processed = enhancer.enhance(15) # 10 optimal

    if output_path:
        processed.save(output_path)

    return processed


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

    processed_img = preprocess_image(input_img, output_img)
    print("Processing Complete.")
