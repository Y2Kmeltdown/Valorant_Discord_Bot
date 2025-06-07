import requests

class vlrAPI():
    def __init__(self):
        self.baseURL = "https://vlrggapi.vercel.app"
        self.contentHeader = {
            "Content-Type": f"application/json"
        }

    def news(self):
        req = self.baseURL + f"/news"
        r = requests.get(url=req, headers=self.contentHeader)
        return r.json()
    
    def stats(self, region:str , timespan:str):
        """
        [region]
        Select a region from the following options:\n
        ["na", "eu", "ap", "sa", "jp", "oce", "mn"]

        [timespan]
        Select a timespan from the following options:\n
        ["30", "60", "90", "all"]
        """
        regionList = ["na", "eu", "ap", "sa", "jp", "oce", "mn"]
        if region not in regionList:
            raise Exception(f"Specified region {region} is not one of the following {regionList}")
        
        timespanList = ["30", "60", "90", "all"]
        if timespan not in timespanList:
            raise Exception(f"Specified timespan {timespan} is not one of the following {timespanList}")
        
        req = self.baseURL + f"/stats?region={region}&timespan={timespan}"
        
        r = requests.get(url=req, headers=self.contentHeader)
        return r.json()
    
    def rankings(self, region:str):
        """
        [region]
        Select a region from the following options:\n
        ["na", "eu", "ap", "la", "la-s", "la-n", "jp", "kr", "gc", "col", "cn", "br", "oce", "mn"]
        """
        regionList = ["na", "eu", "ap", "la", "la-s", "la-n", "jp", "kr", "gc", "col", "cn", "br", "oce", "mn"]
        if region not in regionList:
            raise Exception(f"Specified region {region} is not one of the following {regionList}")

        req = self.baseURL + f"/rankings?region={region}"
        r = requests.get(url=req, headers=self.contentHeader)
        return r.json()
    
    def match(self, matchType:str):
        """
        [matchType]
        Select a matchType from the following options:\n
        ["upcoming", "live_score", "results"]
        """
        matchTypeList = ["upcoming", "live_score", "results"]
        if matchType not in matchTypeList:
            raise Exception(f"Match type must be one of the following {matchType}")

        req = self.baseURL + f"/match?q={matchType}"
        r = requests.get(url=req, headers=self.contentHeader)
        return r.json()
    
    def health(self):
        req = self.baseURL + f"/health"
        r = requests.get(url=req, headers=self.contentHeader)
        return r.json()
   
class valEsportsAPI():
    def __init__(self):
        self.baseURL = "https://vlr.orlandomm.net/api/v1"
        self.contentHeader = {
            "Content-Type": f"application/json"
        }
    def teams(self, page:int = 1, limit:str = "10", region:str = "all", teamid:int = None):
        """
        [page]
        Select which page of information to view as an integer

        [limit]
        Select how many teams to view on the current page

        [status]
        Select a status from the following options:\n
        ["ongoing ", "upcoming ", "completed", "all"]

        [region]
        Select a region from the following options:\n
        ["na", "eu", "ap", "las", "lan", "jp", "kr", "gc", "ch", "br", "oce", "mn", "all"]

        [teamid]
        Overrides all other parameters when not None
        Directly search for an individual team by their team ID
        """
        if teamid is not None:
            req = self.baseURL + f"/teams/{teamid}"
        else:
            regionList = ["na", "eu", "ap", "las", "lan", "jp", "kr", "gc", "ch", "br", "oce", "mn", "all"]
            if region not in regionList:
                raise Exception(f"Specified region {region} is not one of the following {regionList}")
            
            req = self.baseURL + f"/teams?page={page}&limit={limit}&region={region}"
            
        r = requests.get(url=req, headers=self.contentHeader)
        return r.json()
    
    # TODO Get this working not necessary
    def players(self, page:int = 1, limit:int = 10, event_series = "all", event = "all", region:str = "all", country:str = "all", minrounds:int = 200, minrating:int = 1550, agent:str = "all", map = "all", timespan:str = "60d", playerid:int = None):
        if playerid is not None:
            req = self.baseURL + f"/players/{playerid}"
        else:
            #TODO add checks for correct API inputs
            req = self.baseURL + f"/players?page={page}&limit={limit}&event_series={event_series}&event={event}&region={region}&country={country}&minrounds={minrounds}&minrating={minrating}&agent={agent}&map={map}&timespan={timespan}"
        r = requests.get(url=req, headers=self.contentHeader)
        return r.json()
    
    def events(self, page:int = 1, status:str = "all", region:str = "all"):
        """
        [page]
        Select which page of information to view as an integer

        [status]
        Select a status from the following options:\n
        ["ongoing ", "upcoming ", "completed", "all"]

        [region]
        Select a region from the following options:\n
        ["na", "eu", "ap", "las", "lan", "jp", "kr", "gc", "ch", "br", "oce", "mn", "all"]
        """
        statusList = ["ongoing ", "upcoming ", "completed", "all"]
        if status not in statusList:
            raise Exception(f"Status must be one of the following {statusList}")
        
        regionList = ["na", "eu", "ap", "las", "lan", "jp", "kr", "gc", "ch", "br", "oce", "mn", "all"]
        if region not in regionList:
            raise Exception(f"Specified region {region} is not one of the following {regionList}")

        req = self.baseURL + f"/events?page={page}"
        r = requests.get(url=req, headers=self.contentHeader)
        return r.json()
    
    def matches(self):
        req = self.baseURL + f"/matches"
        r = requests.get(url=req, headers=self.contentHeader)
        return r.json()

    def results(self, page:int = 1):
        req = self.baseURL + f"/results?page={page}"
        r = requests.get(url=req, headers=self.contentHeader)
        return r.json()
    

if __name__ == "__main__":

    vlrApp = vlrAPI()
    esports = valEsportsAPI()
    data = esports.results()
    #print(data)
    print(data["data"][0])

    #print(vlrApp.match("upcoming")["data"]["segments"][0])
    # for match in vlrApp.match("upcoming")["data"]["segments"]:
    #     print(match)
    #print(vlrApp.match("results")["data"]["segments"])
    

    pass