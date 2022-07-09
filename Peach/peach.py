import requests
import datetime

class Peach(object):
    def __init__(self,key):
        self.key = key


    def fetch(self,url):
        r = requests.get(url)
        data = r.json()
        return data

    def getName(self,name):
        uuid = self.fetch(url=f'https://api.mojang.com/users/profiles/minecraft/{name}')['id']
        hyapi = self.fetch(f'https://api.hypixel.net/player?key={self.key}&uuid={uuid}')
        return hyapi['player']['name']


    def getUuid(self,name):
        uuid = Pynapple.fetch(f'https://api.mojang.com/users/profiles/minecraft/{name}')['id']
        return uuid

    def getRank(self,name):
        uuid = self.fetch(f'https://api.mojang.com/users/profiles/minecraft/{name}')['id']
        hyapi = self.fetch(f'https://api.hypixel.net/player?key={self.key}&uuid={uuid}')
        return hyapi['player']['newPackageRank']

    def LastLogin(self,name):
        uuid = self.fetch(f'https://api.mojang.com/users/profiles/minecraft/{name}')['id']
        hyapi = self.fetch(f'https://api.hypixel.net/player?key={self.key}&uuid={uuid}')
        return datetime.datetime.fromtimestamp(hyapi['player']['lastLogin'] / 1000)

    def FirstLogin(self,name):
        uuid = self.fetch(f'https://api.mojang.com/users/profiles/minecraft/{name}')['id']
        hyapi = self.fetch(f'https://api.hypixel.net/player?key={self.key}&uuid={uuid}')
        time = hyapi['player']['firstLogin']
        return datetime.datetime.fromtimestamp(time / 1000)

    def LastLogout(self,name):
        uuid = self.fetch(f'https://api.mojang.com/users/profiles/minecraft/{name}')['id']
        hyapi = self.fetch(f'https://api.hypixel.net/player?key={self.key}&uuid={uuid}')
        time = hyapi['player']['lastLogout']
        return datetime.datetime.fromtimestamp(time / 1000)

  
