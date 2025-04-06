import httpx
from app.core.config import settings

class YelpClient:
    def __init__(self):
        self.base_url = settings.YELP_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.YELP_API_KEY}"
        }
        self.client = httpx.AsyncClient()

    async def search_restaurants(self, params: dict):
        response = await self.client.get(
            self.base_url,
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    async def get_business_details(self, business_id: str):
        url = f"https://api.yelp.com/v3/businesses/{business_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()
