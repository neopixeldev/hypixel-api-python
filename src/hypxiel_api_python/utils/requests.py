from aiohttp import ClientSession
# probably need to add a datetime import eventually
# import HypixelAPI object


async def get(endpoint: str, nocache: bool = None):
    """This function will determine whether it should use a cached object or fetch a new one."""
    """`nocache` is a way for the user to bypass the cache"""
    # need to factor in necessary data, e.g. getting/storing a specific request for a UUID rather than the
    # endpoint itself (currently represented as `object` in pseudocode)

    # if endpoint not in cached endpoints or object not in endpoints[endpoint]:
    #    # await fetch
    # elif x time has passed since it was cached or nocache:
    #   await fetch
    # else:
    #    return endpoints[endpoint]
    pass


async def fetch(url: str):
    """This function fetches data from the Hypixel API"""
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
