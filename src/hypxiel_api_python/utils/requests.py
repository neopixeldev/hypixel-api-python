from src.hypxiel_api_python.utils.cache import purge_cache
from urllib.parse import urlparse, parse_qs
from aiohttp import ClientSession
from datetime import datetime


async def get(self, endpoint: str, param: tuple, nocache: bool = None):
    """Determine whether it should use a cached object or fetch a new one."""
    """`nocache` is a way for the user to bypass the cache"""
    await purge_cache(self)
    api = self.hypixel_api
    cached_response = self.hypixel_api.request_cache[param][f"{endpoint.replace('/', '')}.{param[1]}"]
    if not cached_response:
        return await fetch(self=self, url=f"{api.path}/{endpoint}?key={api.key}&{param[0]}={param[1]}")

    elif cached_response["hypixel-api-python"]["timestamp"] + 60 > int(datetime.now().timestamp()) or nocache:
        return await fetch(self=self, url=f"{api.path}/{endpoint}?key={api.key}&{param[0]}={param[1]}")

    else:
        return cached_response["response"]


async def fetch(self, url: str):
    """Fetches data from the Hypixel API"""
    # stored as variables for readability
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    param_name = list(params.keys())[1]
    param_value = params[param_name][0]

    api = self.hypixel_api
    async with ClientSession() as session:
        async with session.get(url) as request:

            # ratelimit
            if request.status == 429:
                # add handling for ratelimiting
                pass
            elif request.status == 200:
                # check if it's successful
                api.request_cache[f"{parsed.path.replace('/', '')}.{[param_value]}"] = {
                    "response": request.json(),
                    "hypixel-api-python": {
                        "timestamp": int(datetime.now().timestamp())
                    }
                }
                return request.json()
            # add more status codes and else statement
