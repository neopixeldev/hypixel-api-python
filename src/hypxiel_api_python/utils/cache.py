from datetime import datetime


# This is currently only set up to purge values that can't be cached for long, e.g. a hypixel player
# Support will need to be added for name caching


async def purge_cache(hypixel_api, /, *, force=False) -> None:
    """
    It purges the cache of old data

    :param hypixel_api: The HypixelAPI object
    :param force: If set to True, it will purge the entire cache. If set to False, it will purge the cache of old data, defaults to False (optional)
    :return: None
    """
    """Purges the cache of old data"""
    requests = hypixel_api.request_cache
    if force:
        hypixel_api.request_cache = {}
        return
    for key in requests:
        if requests[key]["hypixel-api-python"]["timestamp"] + 60 < int(datetime.now().timestamp()):
            del requests[key]
    return
