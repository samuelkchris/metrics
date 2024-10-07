import asyncio
import psutil
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                # Get CPU and memory usage
                cpu_usage = psutil.cpu_percent(interval=1)
                memory_usage = psutil.virtual_memory().percent

                # Send the data as a JSON object
                await websocket.send_json({
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory_usage
                })

                # Wait for 1 second before sending the next update
                await asyncio.sleep(1)
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
                break
            except asyncio.CancelledError:
                logger.info("WebSocket connection cancelled")
                break
            except Exception as e:
                logger.error(f"Error in WebSocket loop: {e}")
                await asyncio.sleep(5)  # Wait for 5 seconds before retrying
    except Exception as e:
        logger.error(f"Unexpected error in WebSocket endpoint: {e}")
    finally:
        logger.info("WebSocket connection closed")

@app.get("/")
async def root():
    return {"message": "System Monitor API"}

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"An error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9091, log_level="info")