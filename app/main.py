import uvicorn
from fastapi import FastAPI
from routers.api import router as api_router
from routers.web import router as web_router

app = FastAPI()
app.include_router(api_router)
app.include_router(web_router)


def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
