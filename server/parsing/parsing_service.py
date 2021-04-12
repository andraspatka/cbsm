import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

import parser

app = FastAPI()


class BPMNtoTextRequest(BaseModel):
    bpmn_di_1: str
    bpmn_di_2: str


@app.post("/parse-bpmn")
def bpmn_to_text(request: BPMNtoTextRequest):
    print(f"Parsing service was called with two bpmn processes...")
    text_1 = parser.convert_bpmn_to_text(request.bpmn_di_1)
    text_2 = parser.convert_bpmn_to_text(request.bpmn_di_2)
    print(f"Texts parsed: text 1: {text_1} text 2: {text_2}")

    response = {
        "text_1": text_1,
        "text_2": text_2
    }

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
