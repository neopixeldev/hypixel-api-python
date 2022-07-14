from datetime import datetime
from aiohttp import ClientSession
from src.hypxiel_api_python.utils.cache import purge_cache
from src.hypxiel_api_python.hypixel import HypixelAPI


async def get(
        hypixel_api: HypixelAPI,
        endpoint: str,
        params: dict[str, str] = {"", ""},
        *,
        nocache: bool = False,
        expiration_time: int = 60,
        ) -> dict:
    """
    If the cache is empty, is older than 60 seconds or the user wants to bypass the cache, fetch a new object.
    Otherwise, return the cached object

    :param hypixel_api: The HypixelAPI object
    :type hypixel_api: HypixelAPI
    :param endpoint: The endpoint you want to fetch data from
    :type endpoint: str
    :param params: The parameters to send to the API
    :type params: dict[str, str]
    :param nocache: Whether to bypass the cache
    :type nocache: bool
    :param expiration_time: The time in seconds after which the cache will expire, defaults to 60
    :type expiration_time: int
    :return: A dictionary containing the response from the Hypixel API.
    """

    await purge_cache(hypixel_api)
    auth_header = {"API-Key": hypixel_api.key}
    cached_response = hypixel_api.request_cache.get(f"{endpoint}.{params}")

    if (
        not cached_response
        or cached_response["hypixel-api-python"]["timestamp"] + expiration_time > int(datetime.now().timestamp())
        or nocache
    ):
        return await fetch(hypixel_api, endpoint, params, auth_header)

    else:
        return cached_response["response"]


async def fetch(
        hypixel_api: HypixelAPI,
        endpoint: str,
        params: dict[str, str],
        headers: dict[str, str],
        ) -> dict:
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
