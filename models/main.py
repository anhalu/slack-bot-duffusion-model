from fastapi import FastAPI
import uvicorn
from PIL import Image
from diffusion_model import *
import base64
import os
from io import BytesIO
from pydantic import BaseModel
from fastapi import status


app = FastAPI()
basedir = os.path.abspath(os.path.dirname(__file__))
gen_model = None


class genInfo(BaseModel): 
    prompt: str
    width_image: int = 512
    height_image: int = 512


class modelInfo(BaseModel):
    device: str = "cuda"
    torch_dtype: int = 16
    num_inference_steps: int = 50
    checkpoint_name: str = "stabilityai/stable-diffusion-2-1"


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


@app.post("/load_models/")
async def load_models(modelInfo: modelInfo):
    # gen_model = DiffusionGenerationV2(device=modelInfo.device, torch_dtype=modelInfo.torch_dtype, num_inference_steps=modelInfo.num_inference_steps)
    # gen_model.load_checkpoint(checkpoint_name=modelInfo.checkpoint_name)
    return {"device": modelInfo.device, "torch_dtype": modelInfo.torch_dtype, "num_inference_steps": modelInfo.num_inference_steps, 
            "checkpoint_name": modelInfo.checkpoint_name}


@app.post("/gen_image/")
async def gen_image(imageInfo: genInfo):
    img = Image.open('models/Image.jpg')
    # # image = gen_model.generate_image(prompt, width=width_image, height=height_image)
    im_file = BytesIO()
    img.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)

    return {"prompt": imageInfo.prompt, "width_image": imageInfo.width_image, "height_image": imageInfo.height_image, "image_base64": im_b64}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8081, reload=True)
