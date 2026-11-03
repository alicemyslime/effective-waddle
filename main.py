from fastapi import FastAPI, HTTPException
from facts import CatFactAPIError, get_facts as fetch_facts, get_random_fact

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/facts")
async def get_facts():
    try:
        return {"facts": await fetch_facts()}
    except CatFactAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/facts/random")
async def get_random_cat_fact():
    '''
    Get a random cat fact from the cat facts API.'''
    try:
        return {"fact": await get_random_fact()}
    except CatFactAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/facts/{index}")
async def get_fact(index: int):
    try:
        facts = await fetch_facts()
    except CatFactAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    if index < 0 or index >= len(facts):
        return {"error": "Index out of range"}
    return {"fact": facts[index]}

@app.get("/facts/count")
async def get_facts_count():
    try:
        facts = await fetch_facts()
    except CatFactAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"count": len(facts)}
