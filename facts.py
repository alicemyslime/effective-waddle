import httpx


CAT_FACTS_API = "https://catfact.ninja"


class CatFactAPIError(Exception):
    pass


async def _get_json(path: str, params: dict[str, int] | None = None) -> object:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{CAT_FACTS_API}/{path}", params=params)
            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise CatFactAPIError("The cat facts API request failed") from exc


async def get_facts() -> list[str]:
    payload = await _get_json("facts", params={"limit": 50})
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise CatFactAPIError("The cat facts API returned an invalid response")

    facts = []
    for record in payload["data"]:
        if not isinstance(record, dict) or not isinstance(record.get("fact"), str):
            raise CatFactAPIError("The cat facts API returned an invalid response")
        facts.append(record["fact"])
    return facts


async def get_random_fact() -> str:
    payload = await _get_json("fact")
    if not isinstance(payload, dict) or not isinstance(payload.get("fact"), str):
        raise CatFactAPIError("The cat facts API returned an invalid response")
    return payload["fact"]
