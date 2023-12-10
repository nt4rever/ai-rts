from fastapi import FastAPI, HTTPException, Security, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
import uvicorn
from http import HTTPStatus
from utils import load_model, rts_predict, convert_url_to_image, convert_file_to_image
import os
from typing import List, Annotated
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY", None)
modal_path = "./store/{0}".format(os.getenv("MODEL", "rts_best_weight.h5"))

if not api_key:
    print("Missing API Key in Environment Variables")
    exit(1)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_header = APIKeyHeader(name="X-API-Key")

model = load_model(modal_path)


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == api_key:
        return api_key_header
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED.value,
        detail="Invalid or missing API Key",
    )


class ImageList(BaseModel):
    images: List[str]


@app.post("/predicts")
async def predict_images(payload: ImageList, key: str = Security(get_api_key)):
    try:
        res = []
        for image in payload.images:
            image = convert_url_to_image(image)
            res.append(rts_predict(model, image))
        return res
    except:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Internal server error",
        )


@app.post("/predict-images")
async def predict_images(files: Annotated[list[bytes], File(default=...)],
                         key: str = Security(get_api_key)):
    try:
        res = []
        for file in files:
            image = convert_file_to_image(file)
            res.append(rts_predict(model, image))
        return res
    except:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Internal server error",
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
