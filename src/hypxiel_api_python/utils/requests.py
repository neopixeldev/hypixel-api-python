from aiohttp import ClientSession
from datetime import datetime


async def get(self, endpoint: str, param: tuple, nocache: bool = None):
    api = self.hypixel_api
    """Determine whether it should use a cached object or fetch a new one."""
    """`nocache` is a way for the user to bypass the cache"""
    cached_value = self.hypixel_api.endpoints[param][endpoint.replace("/", "")]
    if not cached_value:
        return await fetch(self=self, url=f"{api.path}/{endpoint}?key={api.key}&{param[0]}={param[1]}")

    elif cached_value["hypixel-api-python"]["timestamp"] + 60 > int(datetime.now().timestamp()) or nocache:
        return await fetch(self=self, url=f"{api.path}/{endpoint}?key={api.key}&{param[0]}={param[1]}")

    else:
        return cached_value


async def fetch(self, url: str):
    """Fetches data from the Hypixel API"""
    api = self.hypixel_api
    async with ClientSession() as session:
        async with session.get(url) as request:

            # ratelimited
            if request.status == 429:
                # add handling for ratelimiting
                pass
            elif request.status == 200:
                # store in cache
                # check if it's successful
                return request.json()
            # add more status codes and else statement
