from fastapi import FastAPI, APIRouter

from .api.routers.books import router as books_router

app = FastAPI()


app.include_router(books_router)
