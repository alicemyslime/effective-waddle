from fastapi import FastAPI
from facts import facts

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/facts")
async def get_facts():
    return {
        "facts": facts[:50]
    }

@app.get("/facts/{index}")
async def get_fact_by_index(index: int):
    if index < 0 or index >= len(facts):
        return {"error": "Index out of range"}
    return {
        "fact": facts[index]
    }