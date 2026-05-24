from fastapi import FastAPI
from app.routes.entries import router



app = FastAPI()

app.include_router(router)

@app.get("/ping")
def test_check():
    return {"status":"ok"}