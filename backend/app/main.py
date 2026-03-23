from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.core.logger import logger
from app.exceptions import AppBaseException
from app.routers.health import router as health_router
from app.routers.ocr import router as ocr_router
from app.routers.translate import router as translate_router


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
ASSETS_DIR = FRONTEND_DIR / "assets"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppBaseException)
    async def handle_app_exception(
        request: Request,
        exc: AppBaseException,
    ) -> JSONResponse:
        log_method = logger.warning if exc.status_code < 500 else logger.error
        log_method(
            "%s %s -> %s: %s",
            request.method,
            request.url.path,
            exc.status_code,
            exc.message,
        )
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)

    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(translate_router, prefix=settings.api_prefix)
    app.include_router(ocr_router, prefix=settings.api_prefix)

    if ASSETS_DIR.exists():
        app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")
    else:
        logger.warning("Assets directory was not found: %s", ASSETS_DIR)

    @app.get("/", include_in_schema=False)
    async def serve_index():
        index_path = FRONTEND_DIR / "index.html"
        if not index_path.exists():
            raise HTTPException(status_code=404, detail="Файл интерфейса не найден")
        return FileResponse(index_path)

    return app


app = create_app()
