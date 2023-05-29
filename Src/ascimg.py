import click
import os

from Backend.settings import Settings
import Backend.convert as Convert
import Backend.styles as Styles

@click.command()
@click.argument("src", type=click.Path(exists=True, file_okay=True, readable=True))
@click.option("-sc", "--image-scale", default=Settings.image_scale, type=float, show_default=True)
@click.option("-c", "--contrast-factor", default=Settings.contrast_factor, type=float,  show_default=True)
@click.option("-b", "--brightness-factor", default=Settings.brightness_factor, type=float, show_default=True)
@click.option("-sh", "--sharpness-factor", default=Settings.sharpness_factor, type=float, show_default=True)
@click.option("-d", "--density-scale", default=Settings.density_scale, type=str, show_default=True, help="It can be name of builtin scale or custom string.")
@click.option("-so", "--solarize-factor", default=Settings.solarize_factor, type=int, show_default=True)
@click.option("-i", "--invert", is_flag=True, default=Settings.invert, show_default=True)
@click.option("-m", "--mirror", is_flag=True, default=Settings.mirror, show_default=True)
@click.option("--cls", is_flag=True, default=False, show_default=True, help="Clear terminal's screen before output.")
@click.option("--color", default=None, type=click.Choice(tuple(Styles.COLORS.keys()), case_sensitive=False))
def main(src, image_scale, contrast_factor, brightness_factor, 
         sharpness_factor, density_scale, solarize_factor, invert, mirror,
         cls, color):
    """ Convert src image into ascii text. """

    if cls:
        os.system("cls || clear")

    settings = Settings(
        image_scale, contrast_factor, brightness_factor, sharpness_factor,
        density_scale, solarize_factor, invert, mirror
    )
    text = Convert.image_to_ascii(src, settings)

    if color is not None:
        print(Styles.COLORS[color])

    print(text)


if __name__ == "__main__":
    main()
