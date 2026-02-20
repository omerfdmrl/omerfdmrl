import asyncio
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse # Added import

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from ailemdar.config import get_config
from ailemdar.utils.logging import configure_logging
from ailemdar.core.exceptions import AIlemdarError
from web.backend.error_handling import (
    ailemdar_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from web.backend.routers import agents, branches, config, faiss, issues, prs
from web.backend.services.websocket_manager import WebSocketManager

logger = structlog.get_logger(__name__)

ws_manager = WebSocketManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(log_level="INFO", structured=True)
    logger.info("web_ui_starting")
    
    faiss_router = faiss.router
    if hasattr(faiss_router, "set_ws_manager"):
        faiss_router.set_ws_manager(ws_manager)
    
    agents_router = agents.router
    if hasattr(agents_router, "set_ws_manager"):
        agents_router.set_ws_manager(ws_manager)
    
    yield
    
    logger.info("web_ui_shutting_down")


app = FastAPI(
    title="Ailemdar Web UI",
    description="Web interface for AI-powered code review and issue solving",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_exception_handler(AIlemdarError, ailemdar_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(branches.router, prefix="/api/branches", tags=["branches"])
app.include_router(prs.router, prefix="/api/prs", tags=["pull-requests"])
app.include_router(issues.router, prefix="/api/issues", tags=["issues"])
app.include_router(faiss.router, prefix="/api/faiss", tags=["faiss"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.handle_message(websocket, data)
    except Exception:
        ws_manager.disconnect(websocket)

# New route for the root path to serve a light-themed HTML page
# This route takes precedence over the StaticFiles mount for the root path.
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ailemdar Web UI</title>
        <style>
            body {
                font-family: sans-serif;
                background-color: #f0f2f5; /* Light background */
                color: #333; /* Dark text */
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            h1 {
                color: #2c3e50;
            }
            p {
                color: #555;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Ailemdar Web UI</h1>
        <p>This is a basic light-themed page served by the backend.</p>
        <p>If a full frontend application exists in <code>frontend/dist</code>, it would normally be served here.</p>
        <p>Access API docs at <a href="/docs">/docs</a>.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")
