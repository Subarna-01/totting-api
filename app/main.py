import warnings

warnings.filterwarnings("ignore")

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.events import startup, shutdown
from app.core.settings import settings
from app.modules.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    strict_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.ALLOWED_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)


@app.get(f"{settings.API_V1_STR}/health")
async def health():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok"})


app.include_router(users_router, prefix=settings.API_V1_STR)
