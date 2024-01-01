from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile
from dataclasses import asdict
import urllib.parse
import time

from Backend.convert import image_to_ascii
from Backend.settings import Settings

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def parse_settings(data: str) -> Settings:
    data = urllib.parse.unquote_plus(data)
    values = data.split("~")
    if len(values) != 8:
        print(f"ERROR:    Invalid data length: ({len(values)}) {data}")
        return False
    settings = Settings.from_data_list(values)
    print("Generated settings object: ", settings)
    return settings


@api.get("/")
def home():
    return {'status': 200}

@api.get("/defaults/")
def get_default_settings():
    return asdict(Settings())

@api.post("/convert/")
def convert_image(file: UploadFile, settings: str, web: bool = False):
    time_start = time.perf_counter_ns()
    file_stream = file.file

    try:
        settings_obj = parse_settings(settings)
    except Exception as error:
        return {'error': error}

    if settings_obj == False:
        return {'error': 'Invalid data length.'}

    try:
        text = image_to_ascii(file_stream, settings_obj, web_version=web)
    except Exception as error:
        print("ERROR:   ", error)
        return {'error': error}

    time_end = time.perf_counter_ns()
    total_time = time_end-time_start
    return {'time': total_time/1_000_000_000, 'ascii': text, 'error': False}
