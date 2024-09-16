from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

var = "hola"

@app.get("/variable")
def get_variable():
    return {"variable": var}
