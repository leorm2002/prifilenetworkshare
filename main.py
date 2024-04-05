from fastapi import FastAPI
from app.controllers import router as app_router
import uvicorn

app = FastAPI()

app.include_router(app_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="debug", reload=True)
