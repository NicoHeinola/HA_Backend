import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

logger = logging.getLogger(__name__)


class WebServer:
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
        self.host = host
        self.port = port
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        """Setup FastAPI routes."""

        @self.app.post("/api/request")
        async def handle_request(request_data: dict):
            """Handle incoming requests."""
            try:
                logger.info(f"Received request: {request_data}")
                response = {"status": "success", "message": "Request received and processed", "data": request_data}
                return response
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                raise HTTPException(status_code=400, detail=str(e))

    def start(self):
        """Start the web server."""

        logger.info(f"Starting web server on {self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)
