import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
router = APIRouter() 

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/itinerarios")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)