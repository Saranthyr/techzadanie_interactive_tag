from fastapi import FastAPI

from security import router as security_router

app = FastAPI()

app.include_router(security_router)
