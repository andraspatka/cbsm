import json
import os

import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

TWINWORDS_URL = "https://twinword-text-similarity-v1.p.rapidapi.com/similarity/"
TWINWORDS_API_KEY = os.environ.get("TWINWORDS_API_KEY")


class TextSimilarityRequest(BaseModel):
    text_1: str
    text_2: str


@app.post("/text-similarity")
def text_similarity(request: TextSimilarityRequest):
    print(f"Inputs: {request.text_1} {request.text_2}")

    text_1 = request.text_1
    text_2 = request.text_2

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "x-rapidapi-key": TWINWORDS_API_KEY,
        "x-rapidapi-host": "twinword-text-similarity-v1.p.rapidapi.com"
    }

    payload = {
        "text1": text_1,
        "text2": text_2
    }

    response = requests.post(TWINWORDS_URL, data=payload, headers=headers)
    similarity = json.loads(response.content)["similarity"]

    return similarity


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
