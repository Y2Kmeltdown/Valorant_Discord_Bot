import sqlite3
from pathlib import Path
import vlrAPI
from threading import Thread
from datetime import datetime

class vlrDBtemplate():
    def __init__(self, dbFile:Path):
        self.dbFile = dbFile
        self.esportsAPP = vlrAPI.valEsportsAPI()
        self.updateTables()

    def runQuery(self, query:str, data:list=None):
        try:
            with sqlite3.connect(self.dbFile) as conn:
                cursor = conn.cursor()

                if type(query) is list and type(query[0]) is str:
                    if data:
                        if type(data[0]) is list and len(query) == len(data):
                            for statement, datapoints in zip(query, data):
                                cursor.execute(statement, datapoints)
                        else:
                            raise Exception("If multiple queries are provided the same number of data lists also must be provided")
                    else:
                        for statement in query:
                            cursor.execute(statement)
                elif type(query) is str:
                    if data and type(data[0]) is not list:
                        cursor.execute(query, data)
                    else:
                        cursor.execute(query)
                else:
                    raise Exception("query must be a string or list of strings")
                
                conn.commit()
        except sqlite3.OperationalError as e:
            print("Failed to execute query:", e)

    def init_tables(self):
        sql_statements = [
            """
            CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            url TEXT,
            name TEXT NOT NULL,
            img TEXT,
            country TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            url TEXT,
            name TEXT NOT NULL,
            teamTag TEXT,
            country TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT,
            prizepool TEXT,
            dates TEXT,
            country TEXT,
            image TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            team1 TEXT,
            team2 TEXT,
            status TEXT,
            event TEXT,
            tournament TEXT,
            image TEXT,
            date TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            team1 TEXT,
            team2 TEXT,
            score TEXT,
            winner TEXT,
            status TEXT,
            event TEXT,
            tournament TEXT,
            image TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY,
            lastupdate TEXT
            );
            """,
        ]
        self.runQuery(sql_statements)


    def dropTables(self):
        queries = [
            "DROP TABLE IF EXISTS teams;",
            "DROP TABLE IF EXISTS players;",
            "DROP TABLE IF EXISTS events;",
            "DROP TABLE IF EXISTS matches;",
            "DROP TABLE IF EXISTS results;",
        ]
        self.runQuery(queries)

    def updateTeamsTable(self):
        # Get Teams data
        apiData = self.esportsAPP.teams(limit="all")
        if apiData["status"] == "error":
            print("ERROR: Unable to pull data from API")
        else:
            query = '''INSERT INTO teams(id,url,name,img,country)
                VALUES(?,?,?,?,?) '''
            queryList = []
            dataList = []
            for apiPoint in apiData["data"]:
                data = list(apiPoint.values())
                queryList.append(query)
                dataList.append(data)
            self.runQuery(queryList, dataList)

    def updatePlayerTable(self):
        # Get Player Data
        apiData = self.esportsAPP.players(limit="all", timespan="90d")
        if apiData["status"] == "error":
            print("ERROR: Unable to pull data from API")
        else:
            query = '''INSERT INTO players(id,name,country,url,teamtag)
                VALUES(?,?,?,?,?) '''
            queryList = []
            dataList = []
            for apiPoint in apiData["data"]:
                data = list(apiPoint.values())
                queryList.append(query)
                dataList.append(data)
            self.runQuery(queryList, dataList)

    def updateEventsTable(self):
        apiData = self.esportsAPP.events(status="all", region="all")
        if apiData["status"] == "error":
            print("ERROR: Unable to pull data from API")
        else:
            query = '''INSERT INTO events(id,name,status,prizepool,dates,country,image)
                VALUES(?,?,?,?,?,?,?) '''
            queryList = []
            dataList = []
            for apiPoint in apiData["data"]:
                data = list(apiPoint.values())
                queryList.append(query)
                dataList.append(data)
            self.runQuery(queryList, dataList)

    def updateMatchesTable(self):
        apiData = self.esportsAPP.matches()
        if apiData["status"] == "error":
            print("ERROR: Unable to pull data from API")
        else:
            query = '''INSERT INTO matches(id,team1,team2,status,event,tournament,image,date)
                VALUES(?,?,?,?,?,?,?,?) '''
            queryList = []
            dataList = []
            for apiPoint in apiData["data"]:
                data = [
                    apiPoint["id"], 
                    apiPoint["teams"][0]["name"], 
                    apiPoint["teams"][1]["name"], 
                    apiPoint["status"], 
                    apiPoint["event"], 
                    apiPoint["tournament"],
                    apiPoint["img"],
                    apiPoint["utcDate"]
                    ]
                queryList.append(query)
                dataList.append(data)
            self.runQuery(queryList, dataList)

    def updateResultsTable(self):
        apiData = self.esportsAPP.results()
        if apiData["status"] == "error":
            print("ERROR: Unable to pull data from API")
        else:
            query = '''INSERT INTO results(id,team1,team2,score,winner,status,event,tournament,image)
                VALUES(?,?,?,?,?,?,?,?,?) '''
            queryList = []
            dataList = []
            for apiPoint in apiData["data"]:
                data = [
                    apiPoint["id"], 
                    apiPoint["teams"][0]["name"], 
                    apiPoint["teams"][1]["name"], 
                    f"{apiPoint["teams"][0]["score"]}-{apiPoint["teams"][1]["score"]}", 
                    apiPoint["teams"][0]["name"] if apiPoint["teams"][0]["won"] else apiPoint["teams"][1]["name"], 
                    apiPoint["status"], 
                    apiPoint["event"], 
                    apiPoint["tournament"],
                    apiPoint["img"]
                    ]
                queryList.append(query)
                dataList.append(data)
            self.runQuery(queryList, dataList)

    def updateMetadataTable(self):
        id = 1
        updateTime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        metadataQuery = """INSERT OR REPLACE INTO metadata(id, lastupdate)
            VALUES(?,?);"""
        data = [id, updateTime]
        self.runQuery(metadataQuery, data)

    def updateTables(self):
        self.dropTables()
        self.init_tables()
        self.updateMetadataTable()
        self.updateTeamsTable()
        self.updatePlayerTable()
        self.updateEventsTable()
        self.updateMatchesTable()
        self.updateResultsTable()
        pass

    def getLastUpdateTime(self):

        pass

    def getNextPage():
        pass

if __name__ == "__main__":
    dbLocation = Path("data/vlr.db")
    vlrDB = vlrDBtemplate(dbLocation)

        
