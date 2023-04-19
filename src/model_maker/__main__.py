import uvicorn

from model_maker.config import get_config

if __name__ == "__main__":
    uvicorn.run(
        "model_maker.server:app",
        host="0.0.0.0",
        port=8000,
        reload=get_config().debug,
    )
