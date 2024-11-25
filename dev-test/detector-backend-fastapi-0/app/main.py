import signal
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from app.api.main import api_router
from app.api.workers_init import (violence_alarm_detector_worker,
                                  violence_basic_detector_worker)
from app.core.config import settings
from app.modules.violence_detection.task_manager import stop_worker


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(_):
    violence_basic_detector_worker.start()
    violence_alarm_detector_worker.start()
    yield
    signal.signal(signal.SIGINT, lambda sig, frame: stop_worker(
        violence_basic_detector_worker, violence_alarm_detector_worker))


app_args = dict()
if settings.DEBUG:
    app_args.update({
        "openapi_url": f"{settings.API_V1_STR}/openapi.json",
    })

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    **app_args,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
