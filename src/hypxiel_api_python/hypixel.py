# Cache clearing needs to be implemented, create a function for it?

class HypixelAPI:
    """Represents the main class. This will store the API key and cached data"""
    def __init__(self, key):
        self.key = key
        self.path = "https://api.hypixel.net/"
        self.request_cache = {}
