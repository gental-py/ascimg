<img title="Logo" src="https://github.com/gental-py/ascimg/blob/main/assets/logo.png?raw=true" alt="Logo" data-align="inline" width="128">

# ascimg - CLI

### Command Line Interface for Ascimg.

### 🛠️ Changelog:

##### `2.0`:

* Disconnect program from API, now it runs locally.

* Add video support (--video)

* Change clear screen to \033c

* Remove custom --image-scale

* Remove custom --api provider

* Add dynamically updating image scale (based on terminal size)
  
  

## 💻 How to use?

*1.* Clone this repository: (or download manually)

```bash
mkdir ascimg-cli
cd ascimg-cli
git clone https://github.com/gental-py/ascimg_cli
```

*2.* Install required libraries from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## ❔Syntax, params and flags.

Main syntax: `py ascimg.py <src> [args/flags]`

| **FULL FORM**         | **SHORT FORM** | **TYPE** |
| --------------------- | -------------- | -------- |
| `--contrast-factor`   | `-c`           | float    |
| `--brightness-factor` | `-b`           | float    |
| `--sharpness-factor`  | `-sh`          | float    |
| `--density-scale`     | `-d`           | str      |
| `--solarize-factor`   | `-so`          | float    |
| **FLAGS:**            |                |          |
| `--invert`            | `-i`           |          |
| `--mirror`            | `-m`           |          |
| `--cls`               |                |          |
| `--save`              |                |          |
| `--copy`              |                |          |
| `--video`             |                |          |

`--cls`: Clear console's screen before output.

`--save`: Save output content into: `./ascimg-output-<total_time>.txt`

`--copy`: Copy output to system's clipboard.

*You can find description, default values and types of all settings in [API repo](https://github.com/gental-py/ascimg_api)'s description.* 


