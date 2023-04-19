import uvicorn

from pystarter.config import get_config

if __name__ == "__main__":
    uvicorn.run(
        "pystarter.server:app",
        host="0.0.0.0",
        port=8000,
        reload=get_config().debug,
    )
