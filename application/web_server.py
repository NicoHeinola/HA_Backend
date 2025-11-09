import logging
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
import uvicorn

from helpers.common.eventable import Eventable

logger = logging.getLogger(__name__)


class WebServer(Eventable):
    """
    Web server for Home Assistant integration
    This is a REST API server that handles incoming requests to interact with Home Assistant.
    """

    def __init__(self, host: str, port: int):
        """Initialize the web server.

        Args:
            host: The host to bind to
            port: The port to listen on
        """
        super().__init__()

        self.host = host
        self.port = port
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        """Setup FastAPI routes."""

        @self.app.post("/api/test")
        async def test(data: dict = Body(...)):
            """Handle test events."""

            logger.info(f"Received test event with data: {data}")

            run_action = data.get("run_action")

            if run_action:
                self.fire_event("action_triggered", run_action=run_action, **data)

            return JSONResponse(content={"status": "success"}, status_code=200)

    def start(self):
        """Start the web server."""

        logger.info(f"Starting web server on {self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)
