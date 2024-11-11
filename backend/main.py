import os
from fastapi import FastAPI
from api import router
import uvicorn

app = FastAPI(title=f"FastAPI Shard {os.getenv('SHARD', 'unknown').upper()}")

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
