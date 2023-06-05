<img title="Logo" src="https://github.com/gental-py/ascimg/blob/main/assets/logo.png?raw=true" alt="Logo" data-align="inline" width="128">

# ascimg_

### A rich image to text converter.

This project is split into 3 parts: **CLI**, **API** and **WEB** versions. All of these use roughly the same Backend. You can find more details in `readme` located in each part's repo.

## 💻 How to use?
* If you want to use user-friendly interface, checkout this project's [website](https://ascimg.ct8.pl/).
* There is also a **CLI** version of this project that you cane easily download by following the instructions on it's repo.

## 🧠 Backend.

Each version has it's own `/Backend` directory that contains three (*CLI has fourth*) `.py` files. The are mostly the same with just minor changes made because of slightly different expected outcome.

* `settings.py`:  
  Contains settings object definition with attribute for each setting with assigned default value. It also has method to create instance from an Iterable object that contains exactly 8 values.  
  
  | NAME                | DESCRIPTION                                                                                    | TYPE  | DEFAULT |
  | ------------------- | ---------------------------------------------------------------------------------------------- | ----- | ------- |
  | `image_scale`       | Scale image by given factor.                                                                   | float | `1.0`   |
  | `contrast_factor`   | Apply contrast filter with given factor. I recommend using higher contrast for better results. | float | `1.5`   |
  | `brightness_factor` | Apply brightness filter with this factor.                                                      | float | `1.0`   |
  | `sharpness_factor`  | Generates bigger contrast between object's edges.                                              | float | `1.0`   |
  | `solarize_factor`   | Invert all pixel values above a threshold.                                                     | float | `0.0`   |
  | `density_scale`     | There are two built in scales: `short` and `numeric`, however, you can define your own. This scale dynamically generates connection between pixel's brightness and according character from `density_scale`. (There is special section about this system in this file.)                                                                                               | str   | `short` |
  | `invert`            | Invert colors. Dark will pixels will be treaten as light.                                                                                               | bool  | `False` |
  | `mirror`            | Reverse output image in X direction (ABC -> CBA)                                                                                               | bool  | `False` |

* `density.py`:
This file contains just one class that is responsible for: dynamically generating range scale from given text scale, easy wanted pixel accessing using `.get(value: int) -> str` method where `value` is pixel's brightness in range 0-255. (Check out dedicatet section with details about this algorithm). It also allows to save generated object into local register (that's how `short` and `numeric` scales are saved). The register itself is not stored anywhere and is rebuild at every compilation.

* `convert.py`:
This is main backend's file. It contains two functions (one use another) that uses functionalities from other backend modules. Main function: `image_to_ascii(path: str, settings: settings.Settings = settings.Settings(), web_version: bool = False) -> str` uses second: `prepare_image(path: str, settings: settings.Settings = settings.Settings())` to (as name says) prepare image (resize and apply filters) according to passed (or not) `settings` object. 

* `styles.py` (only `CLI` version.):
Initializes `colorama` package and contains `COLORS` const dictionary with stringified names of real colors and their ASCII representations.

## 🤖 Algorithm.
**PROBLEM:** Convert image into ascii characters.
**SOLUTION:** Firstly, we must decide how are we going to treat image. Thankfully to PIL library, we can easily prepare image by resizing and applying various filters on the image. After this process (`prepare_image()` function) we can simply turn it into matrix build from pixels using `.load()` method. At this point, we can turn each pixel into character. But, how can we decide which pixel corresponds to an character? We know, that every pixel has a color represented in RGB values. By using `(R+G+B) /3` formula (`avg`) we get approximated brightness value. As the value will always be somewhere in between 0 and 255 (including both points) we know that, brightness each pixel's brightness can be one of 256 values. This fact lets us build a scale where we split theese 256 values into groups where each group has a corresponding ASCII character. The main built in scale called `short` is this set of characters: `.:-=+*#%@`. As you can see, every next character takes more space than previous one. Using fact that, we can get pixel's brightness and roughly represent it as a character, we must build a scale that connects some values into a character. For example, pixel with brightness equal to 0 is completly black and "invisible", so we can treat it exactly as a space character. In fact, we don't have (however, we can) to assign a individual character for every value, but we can assign group of values into one character (as a 20 brightness pixel is looks almost the same as a pixel with brightness level at 28 and  by converting image into text, we don't expect 1:1 quality.) That's where simple algorithm for converting normal text (like one in `short` scale) into groups of values with associated character. To start, we need to check how much characters do we have to assign. For example, `short` scale contains `10` characters. Than we can calculate `step`'s value by simple division: `256/scale_length`. To ensure, that there will be no floting point value, we will round result of this division and as brightness scale starts from 0, we will add  1 to outcome. Final formula for calculating `step`: `round(256/scale_length)+1`. Now, we can assign characters to range of numbers in between current step and next step. Using `for range_index in range(-1, 256, step)` we can jump by `step` numbers up to 256. To group numbers, we can create built in `range` object that starts with current value: `range_index +1` and leads up to value of next step: `range_index + step +1`. And that's how we get dictionary of `range: character` values. When we know which brightness values accords to which character, we can finally iterate over each pixel of image, calculate its brightness and get corresponding ASCII character. 
