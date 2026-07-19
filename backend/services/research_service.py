from urllib.parse import urlencode

import httpx


class ResearchService:
    async def search(self, query: str) -> str:
        params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get("https://api.duckduckgo.com/", params=params)
            response.raise_for_status()
            data = response.json()

        abstract = data.get("AbstractText") or data.get("RelatedTopics")
        if isinstance(abstract, list):
            return "\n".join(str(item.get("Text", "")) for item in abstract[:5])
        return str(abstract or "No direct result found.")
