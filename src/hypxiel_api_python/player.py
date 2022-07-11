from src.hypxiel_api_python.utils.requests import get
from math import sqrt


class HypixelPlayer:
    def __init__(self, hypixel_api):
        self.hypixel_api = hypixel_api

    # support for names needs to be added
    async def network_level(self, uuid):
        player = await get(self, endpoint="player", param=("uuid", uuid))
        network_experience = player["player"]["networkExp"] if "networkExp" in player["player"] else 0
        network_level = (sqrt((2 * network_experience) + 30625) / 50) - 2.5 if network_experience != 0 else 1
        return network_level

    async def rank(self, uuid):
        player = await get(self, endpoint="player", param=("uuid", uuid))
        if "rank" in player["player"] and not player["player"]["rank"] == "NORMAL":
            return player["player"]["rank"]

        elif "monthlyPackageRank" in player["player"] and not \
                player["player"]["monthlyPackageRank"] == "NONE":
            return player["player"]["monthlyPackageRank"]

        elif "newPackageRank" in player["player"]:
            return player["player"]["newPackageRank"]

        elif "packageRank" in player["player"]:
            return player["player"]["packageRank"]
        else:
            return None
