from datetime import datetime
from aiohttp import ClientSession
from src.hypxiel_api_python.utils.cache import purge_cache
from src.hypxiel_api_python.hypixel import HypixelAPI


async def get(hypixel_api: HypixelAPI, endpoint: str, params: dict[str, str], nocache: bool = None) -> dict:
    """Determine whether it should use a cached object or fetch a new one."""
    """`nocache` is a way for the user to bypass the cache"""
    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"

    await purge_cache(hypixel_api)
    auth_header = {"API-Key": hypixel_api.key}
    try:
        cached_response = hypixel_api.request_cache[f"{endpoint}.{params}"]
        # print(cached_response)
    except KeyError:
        cached_response = None
    # if not cached_response:
    #     return await fetch(self, endpoint, params, auth_header)
    if not cached_response or cached_response["hypixel-api-python"]["timestamp"] + 60 > int(datetime.now().timestamp()) or nocache:
        return await fetch_hypxiel_api(hypixel_api, endpoint, params, auth_header)

    else:
        return cached_response["response"]


async def fetch_hypxiel_api(hypixel_api: HypixelAPI, endpoint: str, params: dict[str, str], headers: dict[str, str]) -> dict:
    """
    Fetches data from the Hypixel API and returns it as a dictionary

    :param hypixel_api: The HypixelAPI object
    :param endpoint: The endpoint you want to fetch data from
    :type endpoint: str
    :param params: The parameters to send to the API
    :type params: dict[str, str]
    :param headers: The headers that are sent with the request
    :type headers: dict[str, str]
    :return: A dictionary containing the response from the Hypixel API.
    """
    HYPIXEL_API_URL = "https://api.hypixel.net"

    async with ClientSession(HYPIXEL_API_URL, headers=headers) as session:
        async with session.get(endpoint, params=params) as request:
            ratelimit_info = {x: y for x, y in request.headers.items() if x.startswith("RateLimit-")}
            # ratelimit
            print(request.status)
            if request.status == 429:
                # add handling for ratelimiting
                pass
            elif request.status == 200:
                # check if it's successful
                response = await request.json()
                hypixel_api.request_cache[f"{endpoint}.{params}"] = {
                    "response": response,
                    "hypixel-api-python": {
                        "timestamp": int(datetime.now().timestamp())
                    }
                }
                hypixel_api.ratelimit_info = ratelimit_info
                return response
            # add more status codes and else statement
