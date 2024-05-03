from fastapi import FastAPI
from app.routes.trade import router as trade_router
import uvicorn

app = FastAPI()

app.include_router(trade_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
