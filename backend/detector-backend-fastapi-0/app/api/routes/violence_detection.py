import numpy as np
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.workers_init import (violence_alarm_detector_worker,
                                  violence_basic_detector_worker)
from app.modules.logger import get_logger
from app.modules.violence_detection.utils.image import imdecode

router = APIRouter()


def image_read(image: UploadFile = File(...)) -> np.ndarray:
    logger = get_logger()

    if image is None:
        raise HTTPException(400, "Require field `image`")

    # if isinstance(image, File):
    #     if not image.content_type.startswith("image"):
    #         raise HTTPException(400, "File content must be 'image'")
    #     buf = image.file.read()
    #     logger.info(f"REQUEST URL: {image.filename}")
    # else:
    #     raise HTTPException(400, "Params type not support!")
    buf = image.file.read()
    # decode image
    if not len(buf):
        raise HTTPException(400, "File empty error!")
    try:
        image = imdecode(buf)
    except Exception:
        raise HTTPException(400, "Image format error!") from None
    return image


@router.post("/detetct/violence/image",
             summary="Violence Detection",
             description="Detect violence in image")
async def test_detection(image: np.ndarray = Depends(image_read)):
    data1 = violence_basic_detector_worker(image).respond_data
    data2 = violence_alarm_detector_worker(image).respond_data
    response = {
        "basic_detection": str(data1),
        "alarm_detection": str(data2),
    }
    return response
