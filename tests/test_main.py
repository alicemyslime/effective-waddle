import unittest
from unittest.mock import AsyncMock, patch

from httpx import ASGITransport, AsyncClient

from facts import CatFactAPIError
from main import app


FACTS = ["Cats sleep a lot.", "Cats use their whiskers to sense."]


class FactsEndpointTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        )

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_list_facts(self):
        with patch("main.fetch_facts", new_callable=AsyncMock) as fetch_facts:
            fetch_facts.return_value = FACTS

            response = await self.client.get("/facts")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"facts": FACTS})
        fetch_facts.assert_awaited_once_with()

    async def test_random_fact(self):
        with patch("main.get_random_fact", new_callable=AsyncMock) as get_random_fact:
            get_random_fact.return_value = FACTS[0]

            response = await self.client.get("/facts/random")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"fact": FACTS[0]})
        get_random_fact.assert_awaited_once_with()

    async def test_individual_fact(self):
        with patch("main.fetch_facts", new_callable=AsyncMock) as fetch_facts:
            fetch_facts.return_value = FACTS

            response = await self.client.get("/facts/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"fact": FACTS[1]})
        fetch_facts.assert_awaited_once_with()

    async def test_individual_fact_index_out_of_range(self):
        with patch("main.fetch_facts", new_callable=AsyncMock) as fetch_facts:
            fetch_facts.return_value = FACTS

            response = await self.client.get("/facts/2")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"error": "Index out of range"})

    async def test_random_fact_reports_upstream_failure(self):
        with patch("main.get_random_fact", new_callable=AsyncMock) as get_random_fact:
            get_random_fact.side_effect = CatFactAPIError("The cat facts API request failed")

            response = await self.client.get("/facts/random")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.json(),
            {"detail": "The cat facts API request failed"},
        )


if __name__ == "__main__":
    unittest.main()
