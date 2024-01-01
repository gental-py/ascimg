from PIL import Image, ImageEnhance, ImageOps

from Backend.settings import Settings
from Backend.density import DensityScale


def prepare_image(path, settings: Settings = Settings()) -> Image.Image:
    """ Load and edit image according to given Settings. """
    image = Image.open(path)
    width, height = image.size

    # Resize.
    image_scale = settings.image_scale
    image = image.resize((round(width*image_scale), round(height*image_scale)))

    # Turn into grayscale.
    image = ImageOps.grayscale(image)

    # Apply image filters.
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(settings.contrast_factor)

    brightness = ImageEnhance.Brightness(image)
    image = brightness.enhance(settings.brightness_factor)

    sharpness = ImageEnhance.Sharpness(image)
    image = sharpness.enhance(settings.sharpness_factor)

    if settings.invert:
        image = ImageOps.invert(image)

    if settings.mirror:
        image = ImageOps.mirror(image)

    image = ImageOps.solarize(image, 256-settings.solarize_factor)
    
    return image

def image_to_ascii(path: str, settings: Settings = Settings(), web_version=False) -> str:
    """ Convert image to ascii characters according to settings. 
    Returns converted image as a string. """
    image = prepare_image(path, settings)
    width, height = image.size
    pixels = image.load()

    density_scale = DensityScale.register.get(settings.density_scale)
    if density_scale is None:
        density_scale = DensityScale(settings.density_scale)

    text = ""
    for y in range(height):
        for x in range(width):
            char = density_scale.get(pixels[x, y])
            if web_version:
                if char == " ":
                    char = "&nbsp;"
            text += char
        if web_version:
            text += "<br>"
        else:
            text += "\n"
    
    return text

