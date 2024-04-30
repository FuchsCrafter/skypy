# skypy(skypy-api) by FuchsCrafter - https://github.com/FuchsCrafter/skypy
# Also check out skypy-webui - https://github.com/FuchsCrafter/skypy-webui

import requests
import json

class skypy:
    """ The main class for the module. Uses an api key"""
    def __init__(self, key:str, blockKeyTest:bool=False) -> None:
        global apikey
        assert key != ""
        apikey = str(key)
        if not blockKeyTest:
            r = requests.get("https://api.hypixel.net/v2/skyblock/news?key="+ key)
            returns = json.loads(r.text)
            returns = returns["success"]
            if not returns:
                print("Invalid API Key! Please note that you cant use some modules now!")


    def getNews(self) -> list:
        """(Requires Authentication) Gets the latest SkyBlock news. """
        r = requests.get("https://api.hypixel.net/v2/skyblock/news?key=" + apikey)
        returns = json.loads(r.text)
        if not returns["success"]:
            print("Failed! Make sure that you api key is correct!")
        else:
            return returns["items"]

    def getItem(self, itemname:str) -> dict:
        """ Gets a specific item and its childs (e.g. NPC sell price, category, name, etc.)"""
        r = requests.get("https://api.hypixel.net/v2/resources/skyblock/items")
        r = json.loads(r.text)["items"]
        try:
            for element in r:
                if element["id"] == itemname:
                    return element
        except:
            return

    def getAllItems(self) -> dict:
        """ Gets all Items and returns them in a disctionary."""
        r = requests.get("https://api.hypixel.net/v2/resources/skyblock/items")
        r = json.loads(r.text)["items"]
        returns = {}
        for element in r:
            returns[element["id"]] = element
        return returns

    def getCurrentBingo(self):
        return json.loads(requests.get("https://api.hypixel.net/v2/resources/skyblock/bingo").text)
    

    class bazaar:
        """ The bazaar class was made to get bazaar values from certain items. """
        def __init__(self):
            pass

        def fetchAllProducts(self) -> dict:
            """ Fetches all products and returns them as a JSON string. """
            return json.loads(requests.get("https://api.hypixel.net/v2/skyblock/bazaar").text)["products"]


        def fetchProduct(self, itemname, quickmode=False) -> dict:
            """ Fetches a specific product and returns his data as a JSON string. Use Quick Mode for shorter but cleaner returns. Returns False if the product is not found. """
            r = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
            bazaarProducts = json.loads(r.text)
            bazaarProducts = bazaarProducts["products"]
            try:
                if not quickmode:
                    return bazaarProducts[itemname]
                else:
                    _ = bazaarProducts[itemname]
                    return _["quick_status"]
            except:
                return False
            
    class auction:
        """ The auction class is there to get auction informations. It requires the Hypixel api key (log into mc.hypixel.net and type /api in chat)."""
        def __init__(self):
            pass

        def getAuctionByPlayer(self, uuid:str) -> list:
            """ Gets the auction by a player uuid. """
            r = requests.get("https://api.hypixel.net/v2/skyblock/auction?key=" + apikey + "&player=" + uuid)
            returns = json.loads(r.text)
            if not returns["success"]:
                print("Failed! Make sure, that you api key and the uuid is correct!")
            else:
                return returns["auctions"]

        def getAuctionByPlayerName(self, player:str) -> list: 
            """ Uses the Mojang API to get the uuid of a player. """
            r = requests.get("https://api.mojang.com/users/profiles/minecraft/" + player) # TODO: Create dedicated function for this
            returns = json.loads(r.text)
            try:
                playeruuid = returns["id"]
            except:
                print("Invalid Playername!")
            else: 
                return self.getAuctionByPlayer(playeruuid)
        
        def getAuctionsByPlayer(self, uuid:str) -> list:
            """Alias function for getAuctionByPlayer"""
            return self.getAuctionByPlayer(uuid=uuid)
            
        def getAuctionsByPlayerName(self, player:str) -> list:
            """Alias function for getAuctionByPlayerName"""
            return self.getAuctionByPlayerName(player=player)

        def getAuction(self, auctionid:str) -> dict:
            """ Gets an auction by its ID. """
            r = requests.get("https://api.hypixel.net/v2/skyblock/auction?key=" + apikey + "&uuid=" + auctionid)
            returns = json.loads(r.text)
            if not returns["success"]:
                print("Failed to get auction! Make sure that you api-key and the auction's ID are both correct!")
                # raise ValueError(f"Incorrect auction ID: {auctionid}") # TODO: Check for error (if it is the invalid API key or the invalid auction id)
            else:
                return returns["auctions"][0]

        def getAuctions(self, page:int=0) -> list:
            """ Gets all active auctions.. """
            r = requests.get("https://api.hypixel.net/v2/skyblock/auctions?page=" + str(page))
            returns = json.loads(r.text)
            return returns["auctions"]
        
        def getAuctionsMetadata() -> dict[str: int]: 
            """ Gets general info about all auctions """
            r = requests.get("https://api.hypixel.net/v2/skyblock/auctions")
            returns = json.loads(r.text)
            out = { "totalPages": returns["totalPages"], "totalAuctions": returns["totalAuctions"], "lastUpdated": returns["lastUpdated"]}
            return out

        def getEndedAuctions(self) -> list:
            """ Gets the latest ended auctions. It works also without any authorization."""
            r = requests.get("https://api.hypixel.net/v2/skyblock/auctions_ended")
            returns = json.loads(r.text)
            return returns["auctions"]
        
        
    class mayor:
        """ The mayor class is there to get the current election results or the current mayor."""
        def __init__(self):
            r = requests.get("https://api.hypixel.net/v2/resources/skyblock/election")
            returns = json.loads(r.text)
            self.currentElectionCache = returns
            pass

        def updateElectionCache(self) -> None:
            r = requests.get("https://api.hypixel.net/v2/resources/skyblock/election")
            returns = json.loads(r.text)
            self.currentElectionCache = returns

        def getCurrentMayor(self, quickmode:bool=False):
            """ Gets the current mayor an his perks. """
            currentMayor = self.currentElectionCache["mayor"]
            if quickmode:
                return {"name": currentMayor["name"],"key": currentMayor["key"]}
            else:
                return currentMayor

        def getCurrentElection(self, quickmode:bool=False, full:bool=True, updateCache:bool=False) -> dict: #TODO: Remaining rewrite, testing
            """ Gets the current election results.
            
            Use the updateCache parameter to update the election cache, or call 
            the updateElectionCache method of the mayor class to do so."""
            if updateCache:
                self.updateElectionCache()
            else:
                returns = self.currentElectionCache
            if "current" in returns:
                if not quickmode:
                    return returns["current"]
                else:
                    _ = returns["current"]["candidates"]
                    returns = {}
                    for element in _:
                        if full:
                            returns[element["name"]] = {"name": element["name"],"key": element["key"], "votes": element["votes"], "perks": element["perks"]}
                        else:
                            returns[element["name"]] = {"name": element["name"],"key": element["key"], "votes": element["votes"]}
                    return returns
            else:
                return False

        def getElectionResults(self, updateCache):  #TODO: Remaining rewrite, testing
            """ Gets only the election votes.

            Use the updateCache parameter to update the election cache, or call 
            the updateElectionCache method of the mayor class to do so."""
            if updateCache:
                self.updateElectionCache()
            else:
                returns = self.currentElectionCache
            if "current" in returns:
                _ = returns["current"]["candidates"]
                returns = {}
                for element in _:
                    returns[element["name"]] = element["votes"]
                return returns
            else:
                return False
    class politics(mayor):
        """# Attention: Class was renamed!
            This class was renamed to 'mayor', but remains as a synonym of 'mayor'. 
            
            Please do not use it when writing new code!
        """
        pass
