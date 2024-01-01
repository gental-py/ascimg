from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError
from dataclasses import dataclass
import pyperclip
import imageio
import click
import time
import sys
import os

def clear_screen():
    print("\033[2j")

@dataclass
class Settings:
    contrast_factor: float = 1.5
    brightness_factor: float = 1.0
    sharpness_factor: float = 1.0
    density_scale: str = "short"
    solarize_factor: float = 0
    invert: bool = False
    mirror: bool = False


class DensityScale:
    register = {}

    def __init__(self, scale: str) -> None:
        self.text_scale = scale
        self.range_scale = self.build_scale()
        
    def build_scale(self) -> dict:
        step = round(256/len(self.text_scale))+1
        range_scale = {}
        
        scale_index = 0
        for range_index in range(-1, 256, step):
            rng = range(range_index+1, range_index+step+1)
            range_scale[rng] = self.text_scale[scale_index]
            scale_index += 1
    
        return range_scale
    
    def get(self, value: int) -> str:
        """ Return character assigned to given pixel's value. """
        for rng, chr in self.range_scale.items():
            if value in rng:
                return chr
            
    def register_scale(self, name: str) -> None:
        """ Save scale to DensityScale.register """
        DensityScale.register[name] = self
            
DensityScale(" .:-=+*#%@").register_scale("short")
DensityScale("0123456789").register_scale("numeric")

        
class Video:
    def __init__(self, path: str):
        self.path = path
        self.reader = imageio.get_reader(self.path)
        self.frame_rate = self.reader.get_meta_data()['fps']
        
    def stream_frames(self):
        for frame in self.reader:
            pillow_image = Image.fromarray(frame)
            yield pillow_image

def prepare_image(path, settings: Settings = Settings()) -> Image.Image:
    """ Load and edit image according to given Settings. """
    if not isinstance(path, Image.Image):
        try:
            image = Image.open(path)
        except UnidentifiedImageError:
            print("Error: failed to open source file. (If it is video, use --video flag)")
            sys.exit(1)
    else:
        image = path
    width, height = image.size

    # Calculate image scale based on terminal size.
    screen_width, screen_height = os.get_terminal_size()
    w_scale = round(screen_width / width, 2)
    h_scale = round(screen_height / height, 2)
    image_scale = min([w_scale, h_scale])

    # Resize.
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

def image_to_ascii(path: str, settings: Settings = Settings()) -> str:
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
            text += char
        else:
            text += "\n"
    
    return text



@click.command()
@click.argument("src", type=click.Path(exists=True, file_okay=True, readable=True))
@click.option("-c", "--contrast-factor", default=Settings.contrast_factor, type=float,  show_default=True)
@click.option("-b", "--brightness-factor", default=Settings.brightness_factor, type=float, show_default=True)
@click.option("-sh", "--sharpness-factor", default=Settings.sharpness_factor, type=float, show_default=True)
@click.option("-d", "--density-scale", default=Settings.density_scale, type=str, show_default=True, help="It can be name of builtin scale or custom string.")
@click.option("-so", "--solarize-factor", default=Settings.solarize_factor, type=int, show_default=True)
@click.option("-i", "--invert", is_flag=True, default=Settings.invert)
@click.option("-m", "--mirror", is_flag=True, default=Settings.mirror)
@click.option("-s", "--speed", default=1.0, type=float, show_default=True)
@click.option("--cls", is_flag=True, default=False, help="Clear terminal's screen before output.")
@click.option("--save", is_flag=True, default=False, help="Save text output to file in current directory.")
@click.option("--copy", is_flag=True, default=False, help="Copy output.")
@click.option("--video", is_flag=True, default=False, help="Convert video frame by frame into text.")
def main(src, contrast_factor, brightness_factor, sharpness_factor, density_scale, 
         solarize_factor, invert, mirror, speed, cls, save, copy, video):
    """ Convert src image into ascii text. """
    if video:
        if any((save, copy)):
            print("Warning: --video flag is ON. Cannot use --copy or --save flag...")

    if cls:
        clear_screen()

    settings = Settings(
        contrast_factor=contrast_factor,
        brightness_factor=brightness_factor,
        sharpness_factor=sharpness_factor,
        density_scale=density_scale,
        solarize_factor=solarize_factor,
        invert=invert,
        mirror=mirror
    )

    if not video:
        output_text = image_to_ascii(src, settings)
        print(output_text)

        if save:
            output_file = "./ascimg-output.txt"
            with open(output_file, "a+") as file:
                file.write(output_text)
            print(f"Output saved to: {output_file}")
        
        if copy:
            pyperclip.copy(output_text)
            print("Copied output to clipboard.")
    
        sys.exit(0)

    if video:
        video_object = Video(src)
        frame_delay = (1/video_object.frame_rate) / speed

        for frame_image in video_object.stream_frames():
            frame_as_text = image_to_ascii(frame_image, settings)
            sys.stdout.write(frame_as_text+"\033[0;0H")
            time.sleep(frame_delay)

        clear_screen()
        sys.exit(0)


if __name__ == "__main__":
    main()
