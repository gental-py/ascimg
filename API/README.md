<img title="Logo" src="https://github.com/gental-py/ascimg/blob/main/assets/logo.png?raw=true" alt="Logo" data-align="inline" width="128">

# ascimg - API

### A brain of entire ascimg project.

This API is currently hosted at: `https://fastapi-production-4d68.up.railway.app/`. You can find list of endpoints with explanation in section below.

## 💻 How to use?
You can either send request to URL above or setup your own API.

#### 🔝 How to setup API?
*1.* Clone this repository: (or download manually)
```bash
mkdir ascimg-api
cd ascimg-api
git clone https://github.com/gental-py/ascimg_api
```

*2.* Install required libraries from `requirements.txt`:
```bash
pip install -r requirements.txt
```

*3.* Run uvicorn server:
```bash
py -m uvicorn api:api --reload
```
Use `--host ?.?.?.? --port ????` to specify `HOST` and `PORT

Now, api should run at specified location or `127.0.0.1:8000`.

(example request using curl: `curl http://127.0.0.1:8000/defaults/`)


## 🎯 Endpoints.
         
| **ENDPOINT** | **TYPE** | **PARAMS**                                                                           | **RETURN**                                                                | **EXPLANATION**                                                                                                                         |
|--------------|----------|--------------------------------------------------------------------------------------|---------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| `/`          | `GET`    | -                                                                                    | `{"status": <int>}`                                                       | `status` should be 200 in most cases. Check if API responds.                                                                            |
| `/defaults/` | `GET`    | -                                                                                    | `{<str>: <float/int/str>}`                                                | {settings_name: default_value}. Return defaults values of all settings.                                                                 |
| `/convert/`  | `GET`    | (FORM BODY: `{"file": UploadFile}` ) QUERY: <`settings`: <str> [`web`: bool = False] | `{"time": <float>, "ascii": <str>, "error": False}` or `{"error": <str>}` | Converts given in FORM BODY `file` according to `settings` in QUERY. `web` flag changes spaces into `&nbsp;` and new lines into `<br>`. |


## 🧠 Backend.

Rough explanation of `Backend/` directory.

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
