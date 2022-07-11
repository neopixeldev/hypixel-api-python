from datetime import datetime

# This is currently only set up to purge values that can't be cached for long, e.g. a hypixel player
# Support will need to be added for name caching


async def purge_cache(self):
    """Purges the cache of old data"""
    requests = self.request_cache
    for key in requests:
        if requests[key]["hypixel-api-python"]["timestamp"] + 60 < int(datetime.now().timestamp()):
            del requests[key]
