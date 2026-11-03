from fastapi import FastAPI
from facts import facts

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/facts")
async def get_facts():
    return {"facts": facts[:50]}