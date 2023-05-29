from dataclasses import dataclass

@dataclass
class Settings:
    image_scale: float = 1.0
    contrast_factor: float = 1.5
    brightness_factor: float = 1.0
    sharpness_factor: float = 1.0
    density_scale: str = "short"
    solarize_factor: int = 0
    invert: bool = False
    mirror: bool = False
