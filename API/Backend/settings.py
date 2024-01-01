from dataclasses import dataclass

@dataclass
class Settings:
    image_scale: float = 1.0
    contrast_factor: float = 1.5
    brightness_factor: float = 1.0
    sharpness_factor: float = 1.0
    density_scale: str = "short"
    solarize_factor: float = 0
    invert: bool = False
    mirror: bool = False

    @staticmethod
    def from_data_list(data_list) -> "Settings":
        scale, contrast, brightness, sharpness, density, solarize, invert, mirror = data_list
        
        if len(density) > 255:
            density = density[:255]

        if float(scale) > 2:
            scale = 2

        return Settings(
            float(scale),
            float(contrast),
            float(brightness),
            float(sharpness),
            str(density),
            float(solarize),
            bool(int(invert)),
            bool(int(mirror))
        )
