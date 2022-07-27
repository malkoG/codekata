from os.path import exists
import os
from pathlib import Path
from time import sleep

from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def unavailable_view():
    flagfile_path = '/tmp/processing_something'
    if exists(flagfile_path):
        raise HTTPException(status_code=503, detail="Already processing contents")
    Path(flagfile_path).touch()
    sleep(30)
    os.remove(flagfile_path)
    return {}